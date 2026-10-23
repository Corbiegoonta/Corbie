#!/usr/bin/env bash
# Microsoft Foundry setup for the Complaint Triage Copilot.
#
# Creates a Foundry resource and project in UK South, deploys one chat model
# and one embedding model, gives you the role you need to call them with your
# `az login` session (no API keys), and writes .env.foundry for the smoke test.
#
# Needs Azure CLI 2.80.0 or later. Run: az login, then bash setup_foundry.sh
# Safe to re-run after fixing an error: each step is a create-or-update.
set -euo pipefail
 
# ---- Settings -----------------------------------------------------------
LOCATION="uksouth"
RG="rg-complaint-copilot"
RES="foundry-nc-copilot"      # becomes a public subdomain: must be globally unique
PROJECT="complaint-copilot"
 
CHAT_MODEL="gpt-5-mini"
CHAT_VERSION="2025-08-07"
EMBED_MODEL="text-embedding-3-small"
EMBED_VERSION="1"
SKU="GlobalStandard"
CHAT_CAPACITY=50              # thousands of tokens per minute: a rate limit, not a charge
EMBED_CAPACITY=50
# -------------------------------------------------------------------------
 
echo "== 0. CLI version and signed-in account =="
az version --query '"azure-cli"' -o tsv
az account show --query "{subscription:name, user:user.name}" -o table
 
echo "== 1. Resource group =="
az group create --name "$RG" --location "$LOCATION" -o none
 
echo "== 2. Foundry resource =="
az cognitiveservices account create \
  --name "$RES" --resource-group "$RG" \
  --kind AIServices --sku S0 --location "$LOCATION" \
  --custom-domain "$RES" --assign-identity \
  --allow-project-management true -o none
 
echo "== 3. Foundry project =="
az cognitiveservices account project create \
  --name "$RES" --resource-group "$RG" \
  --project-name "$PROJECT" --location "$LOCATION" -o none
 
echo "== 4. Versions and deployment types offered in $LOCATION =="
for MODEL in "$CHAT_MODEL" "$EMBED_MODEL"; do
  az cognitiveservices model list --location "$LOCATION" \
    --query "[?model.name=='$MODEL'].{model:model.name, version:model.version, skus:join(',', model.skus[].name)}" \
    -o table
done
 
echo "== 5. Chat deployment =="
az cognitiveservices account deployment create \
  --name "$RES" --resource-group "$RG" \
  --deployment-name "$CHAT_MODEL" \
  --model-name "$CHAT_MODEL" --model-version "$CHAT_VERSION" --model-format OpenAI \
  --sku-name "$SKU" --sku-capacity "$CHAT_CAPACITY" -o none
 
echo "== 6. Embedding deployment =="
az cognitiveservices account deployment create \
  --name "$RES" --resource-group "$RG" \
  --deployment-name "$EMBED_MODEL" \
  --model-name "$EMBED_MODEL" --model-version "$EMBED_VERSION" --model-format OpenAI \
  --sku-name "$SKU" --sku-capacity "$EMBED_CAPACITY" -o none
 
az cognitiveservices account deployment list --name "$RES" --resource-group "$RG" \
  --query "[].{name:name, model:properties.model.name, version:properties.model.version, sku:sku.name, ktpm:sku.capacity, state:properties.provisioningState}" \
  -o table
 
echo "== 7. Inference role for you (Owner alone can't call the models) =="
ME=$(az ad signed-in-user show --query id -o tsv)
RES_ID=$(az cognitiveservices account show --name "$RES" --resource-group "$RG" --query id -o tsv)
az role assignment create \
  --assignee-object-id "$ME" --assignee-principal-type User \
  --role "Cognitive Services OpenAI User" --scope "$RES_ID" -o none \
  || echo "   (role assignment may already exist; carrying on)"
 
echo "== 8. Settings for the smoke test =="
cat > .env.foundry <<EOF
AZURE_OPENAI_BASE_URL=https://${RES}.openai.azure.com/openai/v1/
CHAT_DEPLOYMENT=${CHAT_MODEL}
EMBED_DEPLOYMENT=${EMBED_MODEL}
EOF
cat .env.foundry
echo "Done. The role can take up to 5 minutes to apply before the smoke test passes."
 

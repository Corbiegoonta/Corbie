"""Smoke test for the Foundry chat and embedding deployments.
 
Signs in with your `az login` session through Microsoft Entra ID by default.
Set AZURE_OPENAI_API_KEY to use a key instead.
 
    set -a; source .env.foundry; set +a
    uv run --with "openai>=1.106" --with azure-identity python foundry_smoke_test.py
"""
 
import os
import sys
import time
 
from openai import APIConnectionError, APIStatusError, OpenAI
 
BASE_URL = os.environ["AZURE_OPENAI_BASE_URL"]  # https://<resource>.openai.azure.com/openai/v1/
CHAT_DEPLOYMENT = os.environ.get("CHAT_DEPLOYMENT", "gpt-5-mini")
EMBED_DEPLOYMENT = os.environ.get("EMBED_DEPLOYMENT", "text-embedding-3-small")
 
HINTS = {
    401: "Not authenticated. Run `az login` with the account that owns the resource.",
    403: "No inference role yet. Wait 5 minutes after setup, or check the "
    "'Cognitive Services OpenAI User' role on the resource.",
    404: "Deployment not found. Check CHAT_DEPLOYMENT / EMBED_DEPLOYMENT and the base URL.",
    429: "Rate limited. Wait a minute, or raise the deployment's capacity.",
}
 
 
def make_client() -> OpenAI:
    key = os.environ.get("AZURE_OPENAI_API_KEY")
    if key:
        return OpenAI(base_url=BASE_URL, api_key=key)
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
 
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://ai.azure.com/.default"
    )
    return OpenAI(base_url=BASE_URL, api_key=token_provider)
 
 
def main() -> int:
    client = make_client()
    try:
        start = time.perf_counter()
        response = client.responses.create(
            model=CHAT_DEPLOYMENT,
            input="In one sentence, what does a bank's complaints handler do?",
        )
        ms = (time.perf_counter() - start) * 1000
        print(f"Chat OK ({CHAT_DEPLOYMENT}, {ms:.0f} ms): {response.output_text}")
        print(f"  tokens in/out: {response.usage.input_tokens}/{response.usage.output_tokens}")
 
        start = time.perf_counter()
        result = client.embeddings.create(
            model=EMBED_DEPLOYMENT,
            input=["Final response within eight weeks", "Ombudsman referral rights"],
        )
        ms = (time.perf_counter() - start) * 1000
        dims = len(result.data[0].embedding)
        print(f"Embeddings OK ({EMBED_DEPLOYMENT}, {ms:.0f} ms): {len(result.data)} vectors x {dims} dims")
    except APIStatusError as err:
        print(f"Failed with HTTP {err.status_code}: {err.message}")
        print(f"  Hint: {HINTS.get(err.status_code, 'See the error message above.')}")
        return 1
    except APIConnectionError:
        print(f"Could not reach {BASE_URL}. Check the resource name in AZURE_OPENAI_BASE_URL.")
        return 1
    return 0
 
 
if __name__ == "__main__":
    sys.exit(main())
 

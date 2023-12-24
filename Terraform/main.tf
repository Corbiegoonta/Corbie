terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.85.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "mfrga" {
  name     = "mfrg"
  location = "West Europe"
  tags = {
    environment = "dev"
  }
}

# import {
#   to = azurerm_virtual_network.mfvna
#   id = "subscriptions/04d9f053-d0be-48cf-8d8f-85d19526354a/resourceGroups/mfrg/providers/Microsoft.Network/virtualNetworks/mfvn"
# }

resource "azurerm_virtual_network" "mfvna" {
  name                = "mfvn"
  resource_group_name = azurerm_resource_group.mfrga.name
  location            = azurerm_resource_group.mfrga.location
  address_space       = ["10.123.0.0/16"]
  tags = {
    environment = "dev"
  }
}

resource "azurerm_subnet" "mfsna" {
  name                 = "mfsn"
  resource_group_name  = azurerm_resource_group.mfrga.name
  virtual_network_name = azurerm_virtual_network.mfvna.name
  address_prefixes     = ["10.123.1.0/24"]
}

# import {
#   to = azurerm_network_security_group.mfnsga
#   id = "subscriptions/04d9f053-d0be-48cf-8d8f-85d19526354a/resourceGroups/mfrg/providers/Microsoft.Network/networkSecurityGroups/mfnsg"
# }

resource "azurerm_network_security_group" "mfnsga" {
  name                = "mfnsg"
  location            = azurerm_resource_group.mfrga.location
  resource_group_name = azurerm_resource_group.mfrga.name

  tags = {
    environment = "dev"
  }
}

resource "azurerm_network_security_rule" "mfnsra" {
  name                        = "mfnsr"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.mfrga.name
  network_security_group_name = azurerm_network_security_group.mfnsga.name
}

resource "azurerm_subnet_network_security_group_association" "mfnsgaa" {
  subnet_id                 = azurerm_subnet.mfsna.id
  network_security_group_id = azurerm_network_security_group.mfnsga.id
}

resource "azurerm_public_ip" "mfpia" {
  name                = "mfpi"
  resource_group_name = azurerm_resource_group.mfrga.name
  location            = azurerm_resource_group.mfrga.location
  allocation_method   = "Dynamic"

  tags = {
    environment = "dev"
  }
}

resource "azurerm_network_interface" "mfnia" {
  name                = "mfni"
  resource_group_name = azurerm_resource_group.mfrga.name
  location            = azurerm_resource_group.mfrga.location

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.mfsna.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.mfpia.id
  }

  tags = {
    environment = "dev"
  }
}

resource "azurerm_linux_virtual_machine" "mflvma" {
  name                = "mflvm"
  resource_group_name = azurerm_resource_group.mfrga.name
  location            = azurerm_resource_group.mfrga.location
  size                = "Standard_DS1_v2"
  admin_username      = "adminuser"
  network_interface_ids = [
    azurerm_network_interface.mfnia.id
  ]

  custom_data = filebase64("customdata1.tpl")

  admin_ssh_key {
    username   = "adminuser"
    public_key = file("~/.ssh/mfazurekey.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  provisioner "local-exec" {
    command = templatefile("${var.host_os}-ssh-script.tpl", {
      hostname = self.public_ip_address,
      user = "adminuser"
      identityfile = "~/.ssh/mfazurekey"
    })   
    interpreter = var.host_os == "linux" ? ["bash",  "-c"] : ["Powershell", "-Command"]
    }

  tags = {
    environment = "dev"
  }
}

data "azurerm_public_ip" "mfpiaa" {
  name = azurerm_public_ip.mfpia.name
  resource_group_name = azurerm_resource_group.mfrga.name
}

output "public_ip_address" {
  value       = "${azurerm_linux_virtual_machine.mflvma.name}: ${data.azurerm_public_ip.mfpiaa.ip_address}"
}



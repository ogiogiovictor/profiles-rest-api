# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Use the latest Ubuntu LTS release
  config.vm.box = "ubuntu/jammy64" # Ubuntu 22.04 LTS

  # Increase boot timeout to avoid timeout errors
  config.vm.boot_timeout = 600  # 10 minutes

  # Set up a private network with a static IP to avoid DHCP conflicts
  config.vm.network "private_network", ip: "192.168.56.10"

  # Forward ports
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 22, host: 2222

  # Specify VirtualBox as the provider with more resources
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"  # 2GB RAM
    vb.cpus = 2
    vb.gui = false  # Set to true if you want to see the VM GUI
  end

  # Disable automatic updates that may cause boot delays
  config.vm.provision "shell", inline: <<-SHELL
    sudo systemctl disable apt-daily.service
    sudo systemctl disable apt-daily.timer
    sudo apt-get update && sudo apt-get install -y python3-venv zip
  SHELL
end

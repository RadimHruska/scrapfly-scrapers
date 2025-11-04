#!/usr/bin/expect -f
# Skript pro SSH připojení na jarvis s automatickým zadáním hesla

set timeout 10
set hostname "radim"
set password "Hrusra04"

# Zkuste se připojit
spawn ssh $hostname

# Očekávejte prompt pro heslo nebo hostname
expect {
    "password:" {
        send "$password\r"
    }
    "Password:" {
        send "$password\r"
    }
    "yes/no" {
        send "yes\r"
        expect "password:" {
            send "$password\r"
        }
    }
    "Could not resolve hostname" {
        puts "Chyba: Hostname '$hostname' nelze rozpoznat"
        puts "Zkuste použít plný hostname nebo IP adresu:"
        puts "  ssh uzivatel@jarvis.example.com"
        puts "  ssh uzivatel@192.168.1.100"
        exit 1
    }
    timeout {
        puts "Timeout při připojování"
        exit 1
    }
}

# Interaktivní režim
interact


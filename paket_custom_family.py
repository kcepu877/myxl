import json
from api_request import send_api_request, get_family
from auth_helper import AuthInstance
from ui import clear_screen, pause, show_package_details, render_table

def get_packages_by_family(family_code: str, is_enterprise: bool = False):
    api_key = AuthInstance.api_key
    tokens = AuthInstance.get_active_tokens()
    if not tokens:
        print("No active user tokens found.")
        pause()
        return None
    
    packages = []
    
    data = get_family(api_key, tokens, family_code, is_enterprise)
    if not data:
        print("Failed to load family data.")
        pause()
        return None    
    
    in_package_menu = True
    while in_package_menu:
        clear_screen()
        # Tentukan lebar tabel sesuai panjang judul terpanjang
        table_width = 100

        family_name = data['package_family']["name"]
        print(render_table(f"FAMILY NAME: {family_name}", [], show_headers=False, width=table_width))

        package_variants = data["package_variants"]
        option_number = 1
        variant_number = 1
        
        for variant in package_variants:
            variant_name = variant["name"]
            print(render_table(f"Variant {variant_number}: {variant_name}", [], show_headers=False, width=table_width))
            
            # Siapkan tabel paket untuk variant ini
            variant_table = []
            for option in variant["package_options"]:
                option_name = option["name"]
                price = option["price"]
                code = option["package_option_code"]
                
                variant_table.append([option_number, option_name, f"Rp {price}"])
                
                packages.append({
                    "number": option_number,
                    "name": option_name,
                    "price": price,
                    "code": code
                })
                
                option_number += 1
            
            if variant_table:
                print(render_table("PAKET", variant_table, headers=["No", "Paket", "Harga"], width=table_width))
            
            variant_number += 1

        # Menu kembali
        print(render_table("KEMBALI", [["00", "Kembali ke menu sebelumnya"]], headers=["No", "Keterangan"], width=table_width))
        pkg_choice = input("Pilih paket (nomor): ").strip()
        if pkg_choice == "00":
            in_package_menu = False
            return None

        if not pkg_choice.isdigit():
            print("Input tidak valid. Silakan masukkan nomor yang benar.")
            pause()
            continue
        
        selected_pkg = next((p for p in packages if p["number"] == int(pkg_choice)), None)
        if not selected_pkg:
            print("Paket tidak ditemukan. Silakan masukkan nomor yang benar.")
            pause()
            continue

        is_done = show_package_details(api_key, tokens, selected_pkg["code"])
        if is_done:
            in_package_menu = False
            return None
        
    return packages

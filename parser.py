import openpyxl
import psycopg2
import re
import os



def insert_into_db(conn, part, description, image_path):

    image_path = image_path.upper()
    cur = conn.cursor()
    

    product_sql = "INSERT INTO product (part_number, description) VALUES (%s, %s) ON CONFLICT (part_number) DO UPDATE SET description = EXCLUDED.description;"
    print(product_sql, (part, description))
    cur.execute(product_sql, (part, description))
    
    if re.search(r'IMAGES', image_path):
    
        path_prefix = re.split(r'\s*[:;]?\s*IMAGES', image_path)[0].strip()
        images = re.split(r'\s*[:;]?\s*IMAGES', image_path)[1].strip().split(", ")


        path_prefix = re.sub(r'DISK', 'DISC', path_prefix)
        if path_prefix in ["DISC S1", "DISC S2"]:
            path_prefix = path_prefix.split(" ")[1]
        
        delete_images_sql = "DELETE FROM images WHERE part_number = %s;"
        cur.execute(delete_images_sql, (part,))

        # Insert into images table
        for img in images:
            img = img.rstrip('.')
            if path_prefix not in ["DISC COSTCO", "DISC AMAZON"]:
                if not re.match(r'IMG_\d{4}$', img):  
                    img = "IMG_" + str(img).zfill(4)  
                
            full_path = f"R:\\{path_prefix}\\{img.strip()}.jpg"  

            if os.path.exists(full_path):
                image_sql = "INSERT INTO images (part_number, image_path) VALUES (%s, %s) ON CONFLICT (part_number, image_path) DO NOTHING;"
                print(image_sql, (part, full_path))
                cur.execute(image_sql, (part, full_path))

    
    
    conn.commit()
    cur.close()


conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
)


wb = openpyxl.load_workbook('Product Browse.xlsx')
ws = wb.active


for row in ws.iter_rows(values_only=True, min_row=5): 
    part, description, image_path = row
    insert_into_db(conn, part, description, image_path)


conn.close()
wb.close()
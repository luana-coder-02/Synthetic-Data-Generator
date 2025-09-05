import json
import csv
import random
import uuid
from datetime import datetime, timedelta
import requests
import time
from typing import List, Dict
import pandas as pd
import os
import glob

class SyntheticDataGenerator:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model = "mistral"
        
        self.categories = [
            "Electronics", "Clothing", "Home & Garden", "Sports & Outdoors", 
            "Books", "Health & Beauty", "Toys & Games", "Automotive", 
            "Jewelry", "Kitchen & Dining"
        ]
        
        self.brands = [
            "TechFlow", "StyleCraft", "HomeWorks", "ActiveGear", "BookHub",
            "GlowUp", "PlayMax", "DriveForce", "LuxShine", "ChefMaster",
            "QuantumTech", "EcoStyle", "ComfortZone", "ProSport", "WisdomBooks"
        ]

    def call_ollama(self, prompt: str, max_retries: int = 3) -> str:
        """Llama a Ollama con reintentos en caso de error"""
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.8,
                            "top_p": 0.9,
                            "max_tokens": 300
                        }
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "").strip()
                else:
                    print(f"Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"Intento {attempt + 1} falló: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    
        return ""

    def generate_product(self, product_id: str) -> Dict:
        """Genera un producto sintético usando Mistral"""
        category = random.choice(self.categories)
        brand = random.choice(self.brands)
        
        prompt = f"""Generate a realistic product for e-commerce. Category: {category}, Brand: {brand}

Create ONLY the following format (no extra text):
Name: [product name]
Description: [2-3 sentence product description]
Price: [price as number only, between 10-500]

Example:
Name: Wireless Bluetooth Headphones
Description: Premium wireless headphones with noise cancellation and 30-hour battery life. Features high-quality drivers for exceptional sound clarity. Perfect for music, calls, and travel.
Price: 149.99"""

        response = self.call_ollama(prompt)
        
        product_data = {
            "product_id": product_id,
            "category": category,
            "brand": brand,
            "name": "",
            "description": "",
            "price": 0.0,
            "stock": random.randint(0, 500),
            "rating": round(random.uniform(3.0, 5.0), 1),
            "created_date": datetime.now().isoformat()
        }
        
        try:
            lines = response.split('\n')
            for line in lines:
                if line.startswith('Name:'):
                    product_data["name"] = line.replace('Name:', '').strip()
                elif line.startswith('Description:'):
                    product_data["description"] = line.replace('Description:', '').strip()
                elif line.startswith('Price:'):
                    price_str = line.replace('Price:', '').strip().replace('$', '')
                    try:
                        product_data["price"] = float(price_str)
                    except:
                        product_data["price"] = round(random.uniform(10, 500), 2)
        except:
            product_data["name"] = f"{brand} {category} Product"
            product_data["description"] = f"High-quality {category.lower()} from {brand}. Excellent performance and durability."
            product_data["price"] = round(random.uniform(10, 500), 2)
        
        return product_data

    def generate_review(self, product: Dict) -> Dict:
        """Genera una review sintética para un producto"""
        ratings = [1, 2, 3, 4, 5]
        rating = random.choices(ratings, weights=[5, 10, 15, 35, 35])[0]  # Sesgo hacia ratings altos
        
        reviewer_names = [
            "John D.", "Sarah M.", "Mike R.", "Emily C.", "David L.", "Jessica P.",
            "Chris W.", "Amanda T.", "Ryan K.", "Nicole B.", "Tyler S.", "Megan F."
        ]
        
        prompt = f"""Write a customer review for this product:
Product: {product['name']}
Category: {product['category']}
Rating: {rating}/5 stars

Generate ONLY a realistic customer review (1-3 sentences, natural language, like real Amazon reviews). 
Make it match the {rating}-star rating (1=very negative, 5=very positive).
Do not include "Review:" or any prefix."""

        review_text = self.call_ollama(prompt)
        
        if not review_text:
            fallback_reviews = {
                1: "Poor quality, not worth the money. Disappointed with this purchase.",
                2: "Below average product. Had some issues with quality and performance.",
                3: "Average product, works as expected but nothing special.",
                4: "Good quality product, works well and good value for money.",
                5: "Excellent product! Exceeded my expectations, highly recommend."
            }
            review_text = fallback_reviews[rating]
        
        return {
            "review_id": str(uuid.uuid4()),
            "product_id": product["product_id"],
            "reviewer_name": random.choice(reviewer_names),
            "rating": rating,
            "review_text": review_text.strip(),
            "review_date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
            "verified_purchase": random.choice([True, False])
        }

    def generate_dataset(self, num_products: int = 50, reviews_per_product: tuple = (1, 8)):
        """Genera el dataset completo"""
        print(f"Generando {num_products} productos...")
        
        products = []
        reviews = []
        
        for i in range(num_products):
            print(f"Generando producto {i+1}/{num_products}...")
            
            product_id = f"PROD_{str(uuid.uuid4())[:8]}"
            product = self.generate_product(product_id)
            products.append(product)
            
            num_reviews = random.randint(reviews_per_product[0], reviews_per_product[1])
            for _ in range(num_reviews):
                review = self.generate_review(product)
                reviews.append(review)
            
            time.sleep(0.5)
        
        return products, reviews

    def save_data(self, products: List[Dict], reviews: List[Dict], append=False, custom_suffix=""):
        """Guarda los datos en los archivos especificados"""
        
        if append:
            self._append_data(products, reviews)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            suffix = custom_suffix if custom_suffix else timestamp
            
            products_file = f'products_{suffix}.json'
            with open(products_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, indent=2, ensure_ascii=False)
            print(f"✅ Guardado {products_file}")
            
            products_df = pd.DataFrame(products)
            products_csv = f'products_{suffix}.csv'
            products_df.to_csv(products_csv, index=False, encoding='utf-8')
            print(f"✅ Guardado {products_csv}")
            
            reviews_df = pd.DataFrame(reviews)
            reviews_csv = f'reviews_{suffix}.csv'
            reviews_df.to_csv(reviews_csv, index=False, encoding='utf-8')
            print(f"✅ Guardado {reviews_csv}")
            
            self._show_stats(products, reviews, products_df, append)
    
    def _append_data(self, products: List[Dict], reviews: List[Dict]):
        """Agrega datos a los archivos existentes"""
        
        products_file = 'products.json'
        if os.path.exists(products_file):
            with open(products_file, 'r', encoding='utf-8') as f:
                existing_products = json.load(f)
            existing_products.extend(products)
            with open(products_file, 'w', encoding='utf-8') as f:
                json.dump(existing_products, f, indent=2, ensure_ascii=False)
            print(f"✅ Agregados {len(products)} productos a {products_file}")
        else:
            with open(products_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, indent=2, ensure_ascii=False)
            print(f"✅ Creado {products_file}")
        
        products_df = pd.DataFrame(products)
        reviews_df = pd.DataFrame(reviews)
        
        products_csv = 'products.csv'
        reviews_csv = 'reviews.csv'
        
        if os.path.exists(products_csv):
            products_df.to_csv(products_csv, mode='a', header=False, index=False, encoding='utf-8')
            print(f"✅ Agregados {len(products)} productos a {products_csv}")
        else:
            products_df.to_csv(products_csv, index=False, encoding='utf-8')
            print(f"✅ Creado {products_csv}")
        
        if os.path.exists(reviews_csv):
            reviews_df.to_csv(reviews_csv, mode='a', header=False, index=False, encoding='utf-8')
            print(f"✅ Agregadas {len(reviews)} reviews a {reviews_csv}")
        else:
            reviews_df.to_csv(reviews_csv, index=False, encoding='utf-8')
            print(f"✅ Creado {reviews_csv}")
        
        self._show_stats(products, reviews, products_df, append=True)
    
    def _show_stats(self, products, reviews, products_df, append=False):
        """Muestra estadísticas de los datos generados"""
        print(f"\n📊 Estadísticas:")
        print(f"   - Productos generados: {len(products)}")
        print(f"   - Reviews generadas: {len(reviews)}")
        print(f"   - Promedio de reviews por producto: {len(reviews)/len(products):.1f}")
        
        if not append:
            print(f"\n📈 Productos por categoría:")
            category_counts = products_df['category'].value_counts()
            for category, count in category_counts.items():
                print(f"   - {category}: {count}")
generator = SyntheticDataGenerator()

print("🚀 Iniciando generación de datos sintéticos...")
print("   Usando Mistral via Ollama\n")

products, reviews = generator.generate_dataset(
    num_products=5, 
    reviews_per_product=(1, 3)
)
generator.save_data(products, reviews)
print("\n🎉 ¡Generación completada!")
print("   Archivos creados con timestamp único")

def add_more_products(generator, num_products=10, reviews_per_product=(1, 5)):
    """Agrega productos a los archivos existentes"""
    products, reviews = generator.generate_dataset(num_products, reviews_per_product)
    generator.save_data(products, reviews, append=True)
    return products, reviews

generator = SyntheticDataGenerator()

products, reviews = generator.generate_dataset(num_products=5, reviews_per_product=(1, 3))
generator.save_data(products, reviews, append=True)

new_products, new_reviews = add_more_products(generator, num_products=10, reviews_per_product=(2, 5))
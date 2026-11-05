import pandas as pd
from pathlib import Path

df = pd.read_csv("amazon_alexa.tsv", sep = "\t")
output_dir = Path("Documents")
output_dir.mkdir(exist_ok=True)

for idx, row in df.head(30).iterrows(): 
    review_text = row.get("verified_reviews")
    file_path = output_dir / f"resena_{idx + 1:02d}.txt"
    file_path.write_text(str(review_text), encoding = "utf-8")

print("Todos los archivos convertidos")
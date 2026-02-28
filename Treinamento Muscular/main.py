from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from scipy.sparse import hstack
import uvicorn

app = FastAPI()

# Carregamento seguro
try:
    model = joblib.load('modelo_exercicios.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    X_cats_columns = joblib.load('colunas_categorias.pkl')
    print("✅ Cérebro carregado!")
except:
    print("❌ Erro: Verifique se os arquivos .pkl estão na mesma pasta!")

class Exercicio(BaseModel):
    name: str
    target: str
    bodyPart: str

@app.post("/predict")
def predict_equipment(ex: Exercicio):
    nome_vec = vectorizer.transform([ex.name])
    cat_df = pd.get_dummies(pd.DataFrame([{'target': ex.target, 'bodyPart': ex.bodyPart}]))
    cat_df = cat_df.reindex(columns=X_cats_columns, fill_value=0)
    X_input = hstack([nome_vec, cat_df.values.astype(float)])
    resultado = model.predict(X_input)[0]
    return {"equipment": resultado}

# IMPORTANTE: No Windows/Cursor, rodamos assim:
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

    {
  "equipment": "dumbbell"
}
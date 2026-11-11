
from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import io

app = FastAPI()


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):

    try:
        content = await file.read()

        # Lê o CSV utilizando Pandas
        df = pd.read_csv(io.BytesIO(content))

        return {
            "filename": file.filename,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": df.columns.tolist()
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar CSV: {str(e)}"
        )

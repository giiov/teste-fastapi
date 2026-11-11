
from fastapi import FastAPI, UploadFile, File, HTTPException
import csv
import io

app = FastAPI()


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):

    # Lê o arquivo recebido
    content = await file.read()

    try:
        # Converte o conteúdo para texto
        text = content.decode("utf-8-sig")

        # Faz a leitura do CSV
        reader = csv.DictReader(io.StringIO(text))

        if reader.fieldnames is None:
            raise ValueError("CSV vazio ou inválido")

        data = list(reader)

        return {
            "filename": file.filename,
            "columns": reader.fieldnames,
            "total_rows": len(data),
            "data": data
        }

    except (UnicodeDecodeError, csv.Error, ValueError) as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar CSV: {str(e)}"
        )

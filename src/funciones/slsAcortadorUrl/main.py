from aws_lambda_powertools import Logger
import pyshorteners
import json
from datetime import datetime
import pytz

s = pyshorteners.Shortener(timeout=10)
logger = Logger()

tz = pytz.timezone("America/Lima")
date_utc = datetime.now(tz)
format_date = date_utc.strftime("%Y-%m-%d %H:%M:%S")

def shorturl(_data):
    
    try:
        urls = _data.get("urls")
        shorts_url = []

        for url in urls:
            id = url.get("id")
            number = url.get("number")
            original_url = url.get("original_url")
            
            short_url = s.tinyurl.short(original_url)
            dict = {"id": id, "number": number, "short_url": short_url}
            shorts_url.append(dict)
        
        return {
                "statusCode": 200,
                "status": "success",
                "details": "Todos las urls se acortaron correctamente.",
                "cantidadProcesados": f"{len(urls)}",
                "fechayhora": f"{format_date}",
                "data": shorts_url
            }
    
    except Exception as e:
        logger.exception("Error en send_message " + e)
        raise (e)

# EntryPoint
def lambda_handler(event, context):
    logger.set_correlation_id(context.aws_request_id)
    estado = 200
    respuesta = ""
    logger.set_correlation_id(event)
    try:
        body = event["body"]
        
        if body:
            respuesta = shorturl(body)
            estado = respuesta["statusCode"]
        else:
            estado = 400
            respuesta = {
                "status": "failure",
                "error": "Solicitud inválida. Por favor, verifique los parámetros de entrada.",
                "cantidadProcesados": 0,
                "detalles": [
                    {
                        "codigo": "CuerpoSolicitudVacio",
                        "mensaje": "El cuerpo de la solicitud no puede estar vacío.",
                    }
                ],
            }
    except Exception as e:
        logger.exception(f"error: Error al realizar el servicio: {str(e)}")
        estado = 500
        respuesta = {
            "status": "failure",
            "error": "Error al realizar el servicio, revisar los logs en la consola de AWS CloudWatch.",
        }
    finally:
        return {"statusCode": estado, "body": json.dumps(respuesta)}
    
    
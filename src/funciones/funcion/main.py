
# EntryPoint
def lambda_handler(event, context):
    try: 
        print("Proceso completado con éxito")
        return {
            'statusCode': 200,
            'body': 'Proceso completado con éxito.'
        }
    
    except Exception as e:
        print(f"Error al procesar: {e}")
        return {
                'statusCode': 500,
                'body': 'Error al procesar los datos'
        }



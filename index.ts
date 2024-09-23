import { ServiciosAWS } from "pulumi-serverless-aws";
import { TAGS, GRUPO_LOG } from "./variables"

const sls = new ServiciosAWS();

const capa = sls.crearCapa({
  ruta: "python/sls_utilidades_lambda",
  compatibleRuntimes: ["python3.12"],
  descripcion: "Librerias instaladas: [aws-lambda-powertools==2.39.1, pytz==2024.1](jmespath-1.0.1, typing_extensions-4.12.2)"
})

sls.crearFuncion({
  codigoFuente: {
    ruta: "funcion/main.py"
  },
  handler: "main.lambda_handler",
  descripcion: "lambda creada con libreria para serverles desde pulumi",
  roleArn: "arn:aws:iam::000000000:role/osng_iamlambda-d8f5252",
  nombreGrupoLog: GRUPO_LOG,
  runtime: "python3.12",
  etiquetas: TAGS
})

sls.crearFuncion({
  codigoFuente: {
    ruta: "slsFiltrado/main.py"
  },
  handler: "main.lambda_handler",
  descripcion: "Lambda para filtrar reguistros",
  roleArn: "arn:aws:iam::000000000:role/osng_iamlambdas3recldbcomu-d11fe95",
  nombreGrupoLog: GRUPO_LOG,
  runtime: "python3.12",
  tiempoEjecucion: 10,
  capas: [
    capa.arn
  ],
  etiquetas: TAGS,
  eventos: [
    {
      tipo: "s3",
      parametros: {
        nombreBucket: "dev-osng-informacion-reclamos",
        eventos: [
          "s3:ObjectCreated:Put"
        ],
        prefigo: "dataset_osng_reclamos",
        extencion: ".csv"

      }
    }]
})
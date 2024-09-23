import * as pulumi from "@pulumi/pulumi";

const config = new pulumi.Config();

const ENV = config.require("env")
const EMPRESA = config.require("empresa")
const PROYECTO = config.require("proyecto")

const TAGS = {
  "Entorno": ENV,
  "Propietario": EMPRESA,
  "Proyecto": PROYECTO
}
const GRUPO_LOG = "envio-sms"

export {
  TAGS,
  GRUPO_LOG
}
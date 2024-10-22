# acr-cpp-static-class

Arquivo config.json

```json
{
  "stage": "static",
  "messageNoConstructor": "Por só possuir method static, crie um constructor como deleted (`Constructor = delete;`)<br>Arquivo ${FILE_PATH}<br>Linha: ${LINE_NUMBER}",
  "messageConstructorNoDelete": "Por so possuir method static, ajuste o constructor para deleted (`Constructor = delete;`).<br>Arquivo ${FILE_PATH}<br>Linha: ${LINE_NUMBER}",
  "messageConstructorNoPublic": "Para padronizar, mova o constructor deleted para um method public.<br>Arquivo ${FILE_PATH}<br>Linha: ${LINE_NUMBER}"
}
```

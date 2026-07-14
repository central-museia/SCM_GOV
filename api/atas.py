from api.parser import PNCPParser

resultado = pncp.get(...)

atas = PNCPParser.parse_atas(
    resultado["data"]
)

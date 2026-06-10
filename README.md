# Disparador de PDFs via E-mail

Aplicativo em **Python com interface gráfica** para **envio automático de PDFs por e-mail**. Permite selecionar múltiplos arquivos, gerar destinatários a partir dos nomes dos arquivos e disparar mensagens personalizadas via SMTP.

## O problema que resolve

Enviar dezenas de PDFs individualmente por e-mail é repetitivo e consome horas. Esta ferramenta automatiza todo o fluxo: seleção, personalização e disparo.

## Funcionalidades

- Interface gráfica simples e prática
- Seleção de múltiplos PDFs de uma vez
- Geração de destinatários a partir dos nomes dos arquivos
- Mensagens personalizadas por destinatário
- Envio via SMTP (adaptável a qualquer provedor)

## Tecnologias

- Python 3
- Biblioteca de interface gráfica (Tkinter)
- `smtplib` para envio via SMTP

## Como rodar

```bash
git clone https://github.com/David-Henrique-Cangiani/Disparador-de-PDF-via-e-mail.git
cd Disparador-de-PDF-via-e-mail

python "disparador de email com pdf.py"
```

> **Configuração de e-mail:** informe seu servidor SMTP, e-mail e senha de aplicativo nas configurações do programa. **Nunca** versione credenciais reais no repositório — use senha de app e/ou variáveis de ambiente.

## Autor

**David Henrique Cangiani** — AI Product Builder
[LinkedIn](https://www.linkedin.com/in/david-cangiani-695766212) · [GitHub](https://github.com/David-Henrique-Cangiani)

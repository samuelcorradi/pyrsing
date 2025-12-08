# Pyrsing

## Local environment

**Política de execução do Powershell**

Para ativar o ambiente virtual com o comando `.venv\script\Activate.ps1` é preciso habilitar a execução de scripts do Powershell [1].

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

# Referências

1. https://learn.microsoft.com/pt-pt/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.5
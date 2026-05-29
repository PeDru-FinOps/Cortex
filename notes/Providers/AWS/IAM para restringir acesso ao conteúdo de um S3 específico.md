#aws #cloud8 #cloudcomputing #management #security #data_governance 

Se um usuário questionar uma política de ReadOnlyAccess na AWS, por permitir leitura de conteúdo de todos os buckets, é possível [[Customizar uma política de IAM via JSON na AWS]] com o seguinte escopo:

````
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DenyReadingObjectsFromOtherBuckets",
            "Effect": "Deny",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion"
            ],
            "NotResource": [
                "arn:aws:s3:::<nome-do-bucket>/*"
            ]
        },
        {
            "Sid": "DenyListingOtherBucketsContent",
            "Effect": "Deny",
            "Action": [
                "s3:ListBucket"
            ],
            "NotResource": [
                "arn:aws:s3:::<nome-do-bucket>"
            ]
        }
    ]
}
````

Com isso:

- `ReadOnlyAccess` continua lendo a cloud em geral;
- `s3:ListAllMyBuckets` ainda permite ver que os buckets existem;
- `s3:ListBucket` fica bloqueado para todos, exceto o bucket permitido;
- `s3:GetObject` fica bloqueado para todos, exceto o bucket permitido.

Para o bucket permitido, o próprio `ReadOnlyAccess` já concede a leitura. O `Deny` só remove o acesso dos demais.
## Resultado

### Listagem de todos os buckets

![[Pasted image 20260526154553.png]]

### Permissão de leitura no bucket definido

![[Pasted image 20260526154631.png]]

## Deny nos demais buckets

![[Pasted image 20260526154659.png]]
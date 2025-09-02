from string import Template

htmlTemplate = Template("""
<!DOCTYPE html>
    <head>
        <title>${title}</title>
    </head>
    <body>
        <h1>${page}</h1>
    <body>
<html>
""")

result = htmlTemplate.substitute(title="String Template", page="template substitute")
print(result)

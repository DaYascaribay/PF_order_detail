from flask import Flask
from flask_graphql import GraphQLView
from app.schema import schema

app = Flask(__name__)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True  # interfaz gráfica para testear
    ),
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=1015)

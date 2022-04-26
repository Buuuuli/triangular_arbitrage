from waitress import serve
import new_app

serve(new_app.server, host='localhost',port=3000)
def handle_uploaded_file(f,url):
    with open(url, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
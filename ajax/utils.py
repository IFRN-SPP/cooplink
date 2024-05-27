

# Create your utils here
def is_ajax(request):
  """
  Check if the request is a XMLHttpRequest
  """
  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    return True
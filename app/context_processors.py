from app.models import Cooperative


def global_context(request):
    """
    Middleware or function to add the cooperative to the context.
    """
    context = {}

    cooperative = Cooperative.get_instance()
    context["cooperative"] = cooperative
    return context

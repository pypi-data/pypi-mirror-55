from crosstown_core.models import Stub

stub = Stub(
    pkg="tensorflow",
    git_repo="https://github.com/tensorflow/tensorflow",
    builder_image_prefix="tensorflow-",
    topics=["ml"],
)

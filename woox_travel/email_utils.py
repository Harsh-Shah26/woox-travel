import mimetypes
from pathlib import Path
from email.message import MIMEPart

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from cities_towns_about.models import AboutCityTown


def attach_inline_file(message, file_path, cid_name):
    """
    Attach a local file inline in the email using a Content-ID.
    """
    if not file_path:
        return False

    path = Path(file_path)
    if not path.exists() or not path.is_file():
        return False

    mime_type, _ = mimetypes.guess_type(path.name)
    if not mime_type:
        mime_type = "application/octet-stream"

    maintype, subtype = mime_type.split("/", 1)

    with open(path, "rb") as f:
        content = f.read()

    part = MIMEPart()
    part.set_content(content, maintype=maintype, subtype=subtype)
    part["Content-Disposition"] = "inline"
    part["Content-ID"] = f"<{cid_name}>"
    part["Content-Type"] = mime_type
    message.attach(part)
    return True


def send_reservation_confirmation_email(request, reservation):
    """
    Send professional reservation confirmation email with HTML + text fallback
    and inline city images.
    """
    city_obj = AboutCityTown.objects.filter(act_city_name__iexact=reservation.city).first()

    hero_cid = None
    gallery_cids = []

    subject = f"WoOx Travel Reservation Confirmed - {reservation.city} ({reservation.reservation_id})"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [reservation.email]

    # Build image paths from your media files
    hero_path = None
    gallery_paths = []

    if city_obj:
        if city_obj.act_img:
            hero_path = Path(city_obj.act_img.path)

        for index, image_field in enumerate(
            [city_obj.act_img2, city_obj.act_img3], start=1
        ):
            if image_field:
                gallery_paths.append((Path(image_field.path), f"gallery-image-{index}"))

    context = {
        "reservation": reservation,
        "hero_cid": "hero-image" if hero_path else None,
        "gallery_cids": [{"cid": cid} for _, cid in gallery_paths],
        "site_url": request.build_absolute_uri("/"),
    }

    text_body = render_to_string("reservation_confirmation.txt", context)
    html_body = render_to_string("reservation_confirmation.html", context)

    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=to_email,
    )
    message.attach_alternative(html_body, "text/html")

    if hero_path:
        attached = attach_inline_file(message, hero_path, "hero-image")
        if not attached:
            context["hero_cid"] = None

    for path_obj, cid_name in gallery_paths:
        attach_inline_file(message, path_obj, cid_name)

    message.send(fail_silently=False)
from menu import Menu, MenuItem
from django.core.urlresolvers import reverse

Menu.add_item("main", MenuItem("Overlap",
                               reverse("overlap"),
                               weight=10,
                               icon="tools"))

Menu.add_item("main", MenuItem("Gast",
                               reverse("gast"),
                               weight=20,
                               icon="report"))
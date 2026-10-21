"""Static site generator for ultracleanpnw.com.

Run from the project root:  python _src/build.py
Every page is written as <folder>/index.html so URLs never end in .html.
"""
import json, os
from html import escape
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://ultracleanpnw.com"
NAME = "Ultra Clean PNW"
EMAIL = "info@ultracleanpnw.com"
PHONE = ""  # e.g. "(360) 555-0123". Leave blank to hide phone links.
THEME = "#0a2a4f"

WA_AREAS = ["Vancouver", "Camas", "Washougal", "Battle Ground", "Ridgefield", "La Center",
            "Brush Prairie", "Hazel Dell", "Salmon Creek", "Felida", "Orchards", "Hockinson"]
OR_AREAS = ["Portland", "Beaverton", "Hillsboro", "Lake Oswego", "Tigard", "Tualatin",
            "West Linn", "Milwaukie", "Gresham", "Happy Valley", "Oregon City", "Clackamas"]

# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "check-circle": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "chev-down": '<path d="m6 9 6 6 6-6"/>',
    "chev-right": '<path d="m9 18 6-6-6-6"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "tag": '<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r="1"/>',
    "pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "mountain": '<path d="m8 3 4 8 5-5 5 15H2L8 3z"/>',
    "sparkles": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>',
    "home": '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9 21v-6h6v6"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    "key": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/>',
    "hardhat": '<path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><path d="M14 6a6 6 0 0 1 6 6v3"/>',
    "repeat": '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    "bed": '<path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 17h20M6 8v9"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    "utensils": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2M7 2v20M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/>',
    "sofa": '<path d="M20 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v3"/><path d="M2 16a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v1.5a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5V11a2 2 0 0 0-4 0z"/><path d="M4 18v2M20 18v2"/>',
    "layers": '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>',
    "wind": '<path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "box": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12"/>',
    "monitor": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "door": '<path d="M13 4h3a2 2 0 0 1 2 2v14M2 20h3M13 20h9M10 12v.01"/><path d="M13 4.562v16.157a1 1 0 0 1-1.242.97L5 20V5.562a2 2 0 0 1 1.515-1.94l4-1A2 2 0 0 1 13 4.561Z"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>')


# ---------------------------------------------------------------- images
_SIZES = {}
FOCUS = {"moving": "50% 15%", "eco-bottles": "50% 40%", "bathroom-white": "50% 55%"}


def img(prefix, name, alt, lazy=True, priority=False, sizes=None):
    if name not in _SIZES:
        with Image.open(os.path.join(ROOT, "assets", "img", name + ".jpg")) as im:
            _SIZES[name] = im.size
    w, h = _SIZES[name]
    attrs = 'loading="lazy" decoding="async"' if lazy else 'decoding="async"'
    if priority:
        attrs += ' fetchpriority="high"'
    if name in FOCUS:
        attrs += f' style="object-position:{FOCUS[name]}"'
    return f'<img src="{prefix}assets/img/{name}.jpg" alt="{escape(alt)}" width="{w}" height="{h}" {attrs}>'


# ---------------------------------------------------------------- services
SERVICES = [
    {
        "slug": "residential-cleaning",
        "name": "Residential Cleaning",
        "nav": "Residential Cleaning",
        "icon": "home",
        "card": "Routine whole-home cleaning that keeps kitchens, bathrooms and living spaces fresh, tidy and comfortable.",
        "title": "House Cleaning in Vancouver, WA & Portland, OR | Ultra Clean PNW",
        "desc": "Reliable residential house cleaning in Vancouver, WA and Portland, OR. Kitchens, bathrooms, bedrooms and living areas cleaned with a detailed checklist. Get a free quote.",
        "h1": "Residential cleaning that makes home feel like a reset",
        "intro": "A thorough, room-by-room house cleaning for busy households in Vancouver, Portland and the communities in between. We take care of the dusting, scrubbing and floors so your free time stays free.",
        "img": ("residential", "Bright, freshly cleaned open kitchen and dining area"),
        "gallery": [
            ("window-clean", "Cleaner wiping down a window in a bright home"),
            ("kitchen-wipe", "Gloved hand wiping a kitchen counter with spray cleaner"),
            ("bedroom", "Tidy bedroom with a freshly made bed"),
        ],
        "overview": [
            "Our residential cleaning covers the rooms you use every day. Each visit follows a consistent checklist, so kitchens are wiped down and degreased, bathrooms are scrubbed and sanitized, and every floor is vacuumed and mopped before we leave.",
            "It works as a one-time refresh before guests arrive or as the starting point for a recurring plan. Tell us about any priorities, pets or rooms to skip and we will tailor the visit to your home.",
        ],
        "ideal": ["Busy families", "Working professionals", "Homes with pets", "Renters and homeowners", "Pre-event refresh"],
        "included": [
            ("Kitchen", "utensils", ["Countertops and backsplash wiped and sanitized", "Sink and faucet scrubbed and polished", "Stovetop and appliance exteriors cleaned", "Microwave cleaned inside and out", "Cabinet fronts spot cleaned", "Floors vacuumed and mopped"]),
            ("Bathrooms", "droplet", ["Toilets cleaned inside, outside and at the base", "Showers and tubs scrubbed", "Sinks, vanities and fixtures polished", "Mirrors and glass streak free", "Trash emptied and liners replaced", "Floors washed"]),
            ("Bedrooms and Living Areas", "sofa", ["Dusting of reachable surfaces and decor", "Furniture and shelves wiped", "Beds made and linens changed on request", "Light switches and handles disinfected", "Carpets and rugs vacuumed", "Hard floors mopped"]),
        ],
        "faqs": [
            ("How long does a standard house cleaning take?", "Most homes take between two and four hours depending on size, condition and the number of rooms. We will give you a time estimate along with your quote."),
            ("Do I need to provide cleaning supplies?", "No. Our team arrives with professional supplies and equipment. If you prefer certain products in your home, let us know and we are happy to use them."),
            ("Can you clean around pets?", "Yes. Many of the homes we clean have dogs and cats. Just let us know about any pets ahead of time so we can plan around them."),
        ],
    },
    {
        "slug": "deep-cleaning",
        "name": "Deep Cleaning",
        "nav": "Deep Cleaning",
        "icon": "sparkles",
        "card": "A top-to-bottom detail clean for buildup, baseboards, fixtures and the spots a regular clean skips.",
        "title": "Deep Cleaning Services in Vancouver, WA & Portland, OR | Ultra Clean PNW",
        "desc": "Top-to-bottom deep cleaning in Vancouver, WA and Portland, OR. Baseboards, grout, fixtures, vents and built-up grime handled in detail. Request a free deep clean quote.",
        "h1": "Deep cleaning for the details everyone else misses",
        "intro": "When a home needs more than a surface clean, our deep cleaning goes after built-up grime, soap scum and dust in the places that are easy to overlook. It is the ideal first visit and a great seasonal reset.",
        "img": ("deep-clean", "Cleaner using a steam cleaner on a radiator"),
        "gallery": [
            ("stovetop", "Hand degreasing a gas stovetop with a microfiber cloth"),
            ("bathroom", "Spotless modern bathroom with glass shower and vanity"),
            ("tile-scrub", "Brush scrubbing soapy tile floor and grout lines"),
        ],
        "overview": [
            "A deep clean includes everything in our residential service, plus detailed work that brings a home back to a true baseline. We hand wipe baseboards and door frames, scrub grout, descale fixtures, degrease the kitchen and clear dust from vents, blinds and high ledges.",
            "We recommend a deep clean for a first visit, after a busy season, before or after hosting, or any time the home needs a full reset. Many clients follow it with recurring cleaning to keep that level of clean in place.",
        ],
        "ideal": ["First-time clients", "Seasonal resets", "Before or after hosting", "Homes listed for sale", "Post-illness refresh"],
        "included": [
            ("Detail Work Throughout", "layers", ["Baseboards and door frames hand wiped", "Doors, light switches and outlets cleaned", "Vents, blinds and window sills dusted", "High ledges and ceiling fan blades", "Lamps, frames and decor detailed", "Edges and corners vacuumed"]),
            ("Kitchen", "utensils", ["Stovetop and range hood degreased", "Backsplash and grout scrubbed", "Cabinet fronts and handles washed", "Appliance exteriors polished", "Microwave interior steam cleaned", "Sink drain and disposal area scrubbed"]),
            ("Bathrooms", "droplet", ["Soap scum and hard water buildup removed", "Tile and grout scrubbed", "Fixtures and shower heads descaled", "Behind and around the toilet cleaned", "Cabinet fronts and drawer pulls wiped", "Exhaust fan cover dusted"]),
        ],
        "faqs": [
            ("What is the difference between a standard clean and a deep clean?", "A standard clean maintains a home that is already in good shape. A deep clean adds detailed tasks like baseboards, grout, fixtures, vents and built-up grime, so it takes longer and covers more ground."),
            ("How often should I schedule a deep clean?", "Most households benefit from a deep clean two to four times a year, or as a first visit before starting a recurring plan."),
            ("Can I add inside the oven or fridge?", "Yes. Inside the oven, inside the fridge and interior windows can be added to any deep clean. Just mention them when you request your quote."),
        ],
    },
    {
        "slug": "recurring-cleaning",
        "name": "Recurring Cleaning",
        "nav": "Recurring Cleaning",
        "icon": "repeat",
        "card": "Weekly, bi-weekly or monthly visits on a schedule that fits, so your home stays consistently clean.",
        "title": "Weekly & Bi-Weekly House Cleaning in Vancouver & Portland | Ultra Clean PNW",
        "desc": "Recurring weekly, bi-weekly and monthly house cleaning in Vancouver, WA and Portland, OR. A consistent clean on a schedule that works for you. Get a free quote.",
        "h1": "Recurring cleaning that keeps your home ready every day",
        "intro": "Stop scheduling one cleaning at a time. With a recurring plan, the same standard of clean shows up on a set schedule, and your home stays guest ready without you having to think about it.",
        "img": ("living-bright", "Bright, tidy living room with neutral decor"),
        "gallery": [
            ("mopping", "Mop gliding across a polished hardwood floor"),
            ("spray-wipe", "Gloved hands spraying and wiping a table surface"),
            ("kitchen-white", "Clean white kitchen with clear countertops"),
        ],
        "overview": [
            "Recurring cleaning covers all of the essentials on every visit: kitchens, bathrooms, dusting and floors. Because we visit regularly, we also rotate through detail tasks over time so nothing builds up between appointments.",
            "Choose weekly, every two weeks or monthly, and keep the same day and time slot whenever possible. Need to skip or move a visit for a trip or a holiday? Just let us know ahead of time.",
        ],
        "ideal": ["Busy households", "Dual-income families", "Homes with kids or pets", "Seniors who want a hand", "Anyone who hates scheduling"],
        "included": [
            ("Weekly", "calendar", ["Best for busy homes with kids or pets", "Kitchen and bathrooms cleaned every visit", "Floors vacuumed and mopped weekly", "Fastest visits with the lowest buildup", "One rotating detail task each week"]),
            ("Every Two Weeks", "repeat", ["Our most popular schedule", "Full kitchen and bathroom clean", "Dusting of surfaces and decor", "All floors vacuumed and mopped", "Rotating detail tasks over the month"]),
            ("Monthly", "clipboard", ["A steady monthly reset", "Kitchen and bathrooms scrubbed", "Thorough dusting throughout", "Floors vacuumed and mopped", "Great for smaller or lightly used homes"]),
        ],
        "faqs": [
            ("Do I need a deep clean before starting a recurring plan?", "If the home has not been professionally cleaned recently, we usually recommend starting with a deep clean. It sets a strong baseline so every recurring visit can focus on upkeep."),
            ("Can I change my schedule later?", "Yes. You can switch between weekly, bi-weekly and monthly, or pause service, with notice ahead of your next visit."),
            ("Will I have the same cleaner each time?", "We aim to keep a consistent team on your home so they learn your preferences, though staffing can occasionally vary."),
        ],
    },
    {
        "slug": "move-in-move-out-cleaning",
        "name": "Move-In & Move-Out Cleaning",
        "nav": "Move-In / Move-Out",
        "icon": "box",
        "card": "Empty-home cleaning that gets a property ready for new owners, new tenants or a final walkthrough.",
        "title": "Move-In & Move-Out Cleaning in Vancouver, WA & Portland, OR | Ultra Clean PNW",
        "desc": "Move-in and move-out cleaning in Vancouver, WA and Portland, OR. Inside cabinets, appliances, closets and floors cleaned for walkthroughs, deposits and new owners. Free quote.",
        "h1": "Move-in and move-out cleaning for a smooth handoff",
        "intro": "Moving is a lot of work already. We clean the empty home from the inside of every cabinet to the last baseboard, so it is ready for a walkthrough, a new tenant or your first night in a new place.",
        "img": ("moving", "Woman unpacking moving boxes with her dog in a new home"),
        "gallery": [
            ("empty-room", "Empty, freshly cleaned room ready for move-in"),
            ("empty-kitchen", "Clean, empty kitchen ready for new occupants"),
            ("carpet", "Carpet being deep cleaned with an extraction machine"),
        ],
        "overview": [
            "An empty home shows everything. Our move cleaning focuses on the areas landlords, property managers and buyers check most: inside cabinets and drawers, inside appliances, closets, baseboards, window tracks and every floor.",
            "We work with renters hoping to leave a rental in great shape, homeowners preparing to list or hand over keys, and families who want a fresh, clean start before unpacking. Schedule as soon as the home is empty for the best results.",
        ],
        "ideal": ["Renters moving out", "Homeowners selling", "Landlords and property managers", "Real estate agents", "New homeowners"],
        "included": [
            ("Kitchen", "utensils", ["Inside all cabinets and drawers", "Inside the refrigerator and freezer", "Inside the oven and microwave", "Countertops, sink and backsplash", "Appliance exteriors and range hood", "Floors cleaned edge to edge"]),
            ("Bathrooms", "droplet", ["Inside vanities, drawers and medicine cabinets", "Showers, tubs and tile scrubbed", "Toilets sanitized inside and out", "Mirrors, glass and fixtures polished", "Exhaust fan cover dusted", "Floors and baseboards washed"]),
            ("Throughout the Home", "door", ["Inside closets and shelving", "Baseboards, doors and door frames", "Window sills and tracks", "Light switches, outlets and fixtures", "Blinds dusted", "Carpets vacuumed and hard floors mopped"]),
        ],
        "faqs": [
            ("Does the home need to be empty?", "Yes, for the best results. An empty home lets us reach inside cabinets, closets and along every wall. If a few items remain, let us know when booking."),
            ("Will this help me get my deposit back?", "Our move-out clean targets the areas that are checked during walkthroughs. Final deposit decisions are up to your landlord, but a professional clean gives you the best possible start."),
            ("Do you work with property managers?", "Yes. We can coordinate access and timing with landlords, property managers and real estate agents for turnovers between tenants or before a listing."),
        ],
    },
    {
        "slug": "commercial-cleaning",
        "name": "Commercial Cleaning",
        "nav": "Commercial Cleaning",
        "icon": "building",
        "card": "Office and commercial cleaning that keeps workspaces, restrooms and common areas sharp for staff and clients.",
        "title": "Commercial & Office Cleaning in Vancouver, WA & Portland, OR | Ultra Clean PNW",
        "desc": "Commercial and office cleaning in Vancouver, WA and Portland, OR. Workspaces, restrooms, break rooms and entries cleaned on a schedule that fits your business. Free quote.",
        "h1": "Commercial cleaning that keeps your business looking sharp",
        "intro": "Your space is the first impression clients get and the place your team spends the day. We keep offices and commercial spaces clean, sanitized and presentable on a schedule built around your hours.",
        "img": ("commercial", "Cleaning crew vacuuming and wiping glass walls in an office"),
        "gallery": [
            ("office", "Clean open office with workstations and natural light"),
            ("office-night", "Cleaner mopping an office floor after hours"),
            ("office-desk", "Tidy office desk area with plants and windows"),
        ],
        "overview": [
            "We clean offices, retail spaces, studios and other commercial properties across Clark County and the Portland metro. Every plan is built around your space, foot traffic and hours, with service available before opening, after close or on weekends.",
            "Expect consistent attention to the areas people notice most: entries, restrooms, break rooms, desks and floors. We set a clear checklist with you up front so everyone knows exactly what gets done on each visit.",
        ],
        "ideal": ["Professional offices", "Retail shops", "Studios and showrooms", "Small warehouses with office space", "Building common areas"],
        "included": [
            ("Workspaces", "monitor", ["Desks and work surfaces wiped", "Phones, keyboards and touch points disinfected", "Trash and recycling emptied", "Conference rooms reset", "Glass partitions and doors cleaned", "Carpets vacuumed"]),
            ("Restrooms and Break Rooms", "droplet", ["Toilets, urinals and sinks sanitized", "Mirrors and fixtures polished", "Paper and soap restocked from your supply", "Counters, tables and sinks cleaned", "Microwave and appliance exteriors wiped", "Floors washed"]),
            ("Entries and Common Areas", "door", ["Entry glass and door handles cleaned", "Reception desks and waiting areas tidied", "Dusting of ledges and decor", "Hallways and stairwells vacuumed", "Hard floors swept and mopped", "Spot cleaning of walls and doors"]),
        ],
        "faqs": [
            ("Can you clean after business hours?", "Yes. Most of our commercial clients prefer early morning, evening or weekend service so cleaning never interrupts the workday."),
            ("How often should an office be cleaned?", "It depends on size and foot traffic. Many offices choose one to three visits per week, while busier spaces may need daily service. We will recommend a schedule after a walkthrough."),
            ("Do you offer a walkthrough before quoting?", "Yes. For commercial spaces we prefer a quick walkthrough so we can understand the layout, priorities and access before giving an accurate quote."),
        ],
    },
    {
        "slug": "post-construction-cleaning",
        "name": "Post-Construction Cleaning",
        "nav": "Post-Construction",
        "icon": "hardhat",
        "card": "Fine dust, debris and residue removed after builds and remodels so the space is ready to move in.",
        "title": "Post-Construction Cleaning in Vancouver, WA & Portland, OR | Ultra Clean PNW",
        "desc": "Post-construction and remodel cleaning in Vancouver, WA and Portland, OR. Drywall dust, debris, stickers and residue removed so new spaces are move-in ready. Free quote.",
        "h1": "Post-construction cleaning, from job site to move-in ready",
        "intro": "New builds and remodels leave behind a fine layer of dust that settles everywhere. We remove the dust, debris and residue so your finished space looks the way it was designed to.",
        "img": ("construction-vacuum", "Cleaner vacuuming construction dust from a new concrete floor"),
        "gallery": [
            ("construction-site", "Crew working on an active construction site"),
            ("floor-machine", "Floor scrubbing machine cleaning a newly finished floor"),
            ("finished-interior", "Finished, clean modern interior after construction"),
        ],
        "overview": [
            "Drywall dust and construction debris get into vents, cabinets, light fixtures and window tracks. Our post-construction cleaning works from the top down with HEPA vacuums and microfiber, clearing fine dust from every surface before detailing floors, glass and fixtures.",
            "We work with homeowners after a remodel as well as builders and contractors who need a space ready for a final walkthrough or handoff. We can schedule a rough clean during the project and a final clean at the finish.",
        ],
        "ideal": ["Homeowners after a remodel", "General contractors", "Home builders", "Property developers", "Tenant improvement projects"],
        "included": [
            ("Dust and Debris Removal", "wind", ["Fine drywall dust removed from all surfaces", "Vents, returns and fan blades cleaned", "Light fixtures and switch plates detailed", "Inside cabinets, drawers and closets", "Window sills and tracks vacuumed", "Leftover debris cleared"]),
            ("Surfaces and Fixtures", "sparkles", ["Stickers, labels and tape residue removed", "Paint specks and overspray spot cleaned", "Glass, mirrors and windows streak free", "Countertops and backsplash polished", "Appliances cleaned inside and out", "Plumbing fixtures shined"]),
            ("Final Detail", "check-circle", ["Baseboards, doors and trim wiped", "Hard floors vacuumed and washed", "Carpets vacuumed thoroughly", "Bathrooms fully cleaned", "Entry and garage swept on request", "Final walkthrough ready"]),
        ],
        "faqs": [
            ("When should post-construction cleaning be scheduled?", "Once trades are finished and the space is safe to access. For larger projects, we often do a rough clean near the end of construction and a final clean right before the walkthrough."),
            ("Do you remove large debris or construction materials?", "We clear dust, small debris and residue. Large materials, dumpsters and hauling should be handled by your contractor before we arrive."),
            ("Do you work directly with contractors?", "Yes. We regularly coordinate with builders, contractors and property managers on timing, access and final walkthroughs."),
        ],
    },
    {
        "slug": "airbnb-vacation-rental-cleaning",
        "name": "Airbnb & Vacation Rental Cleaning",
        "nav": "Airbnb & Vacation Rentals",
        "icon": "bed",
        "card": "Reliable turnovers between guests with fresh linens, restocked essentials and a guest-ready reset.",
        "title": "Airbnb & Vacation Rental Cleaning in Vancouver & Portland | Ultra Clean PNW",
        "desc": "Airbnb and short-term rental turnover cleaning in Vancouver, WA and Portland, OR. Fresh linens, restocked essentials and a consistent guest-ready reset. Get a free quote.",
        "h1": "Airbnb and vacation rental cleaning hosts can count on",
        "intro": "Great reviews start with a spotless arrival. We turn your rental over between guests with a consistent checklist, fresh linens and a staged, welcoming space that matches your listing photos.",
        "img": ("rental-bedroom", "Freshly made bed with crisp linens in a rental bedroom"),
        "gallery": [
            ("rental-living", "Clean, staged living room in a short-term rental"),
            ("bedroom", "Guest bedroom with fresh bedding and tidy nightstands"),
            ("bathroom-white", "Clean white bathroom ready for the next guest"),
        ],
        "overview": [
            "Short-term rentals run on tight windows. We work around your check-out and check-in times to clean, reset and stage the property so every guest walks into the same clean, consistent space.",
            "Each turnover includes a full clean of the kitchen, bathrooms and living areas, a linen change, and a reset of the little details guests notice. We will also let you know about anything that needs your attention, like low supplies or damage.",
        ],
        "ideal": ["Airbnb hosts", "VRBO owners", "Short-term rental managers", "Furnished corporate rentals", "Guest suites and ADUs"],
        "included": [
            ("Turnover Clean", "sparkles", ["Kitchen cleaned and dishes put away", "Bathrooms scrubbed and sanitized", "Dusting and surface wipe down", "Trash and recycling removed", "Floors vacuumed and mopped", "Fridge checked for leftover items"]),
            ("Guest-Ready Reset", "bed", ["Beds made with fresh linens", "Towels replaced and folded", "Furniture and decor staged to your photos", "Toiletries and paper goods restocked from your supply", "Coffee station and kitchen essentials reset", "Final walkthrough before check-in"]),
            ("Host Support", "message", ["Flexible same-day turnovers", "Notes on low supplies", "Damage or issue reports to the host", "Lockbox and smart lock friendly", "Consistent checklist every stay", "Deep cleans between busy seasons"]),
        ],
        "faqs": [
            ("Can you handle same-day turnovers?", "Yes. We schedule around your check-out and check-in times. Share your booking calendar and we will plan turnovers to match."),
            ("Do you do laundry?", "We change linens and towels on every turnover. Laundry options depend on the property setup, so let us know if you have an on-site washer and dryer or a linen service."),
            ("Will you let me know about damage or missing items?", "Yes. If we notice damage, missing items or low supplies, we will let you know right away so you can address it before the next guest arrives."),
        ],
    },
]
BY_SLUG = {s["slug"]: s for s in SERVICES}


# ---------------------------------------------------------------- layout
def head(prefix, title, desc, path, jsonld, og_image="assets/og-image.jpg"):
    url = SITE + path
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    return f"""<!DOCTYPE html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="{THEME}">
<meta name="author" content="{NAME}">
<meta name="geo.region" content="US-WA">
<meta name="geo.placename" content="Vancouver, Washington">
<meta name="geo.position" content="45.6387;-122.6615">
<meta name="ICBM" content="45.6387, -122.6615">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME} logo over the Portland skyline">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(desc)}">
<meta name="twitter:image" content="{SITE}/{og_image}">
<link rel="icon" href="{prefix}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{prefix}assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{prefix}assets/favicon-16.png">
<link rel="apple-touch-icon" href="{prefix}assets/apple-touch-icon.png">
<link rel="manifest" href="{prefix}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}css/styles.css">
{ld}
</head>
"""


def header(prefix, active=""):
    def cur(key):
        return ' aria-current="page"' if key == active else ""
    drop = "\n".join(f'<a href="{prefix}services/{s["slug"]}/"{cur(s["slug"])}>{s["nav"]}</a>' for s in SERVICES)
    mob = "\n".join(f'<a href="{prefix}services/{s["slug"]}/">{s["nav"]}</a>' for s in SERVICES)
    home = prefix or "./"
    return f"""<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{home}" aria-label="{NAME} home">
      <img src="{prefix}assets/logo.png" alt="{NAME}" width="520" height="{LOGO_H}">
    </a>
    <nav class="nav" aria-label="Main">
      <ul class="nav-list">
        <li><a class="nav-link" href="{home}"{cur("home")}>Home</a></li>
        <li class="has-dropdown">
          <a class="nav-link" href="{prefix}services/"{' aria-current="page"' if active.startswith("svc") or active in BY_SLUG else ""}>Services {icon("chev-down")}</a>
          <div class="dropdown">
{drop}
<a class="all" href="{prefix}services/">View all services</a>
          </div>
        </li>
        <li><a class="nav-link" href="{prefix}#areas">Service Areas</a></li>
        <li><a class="nav-link" href="{prefix}#about">About</a></li>
        <li><a class="nav-link" href="{prefix}contact/"{cur("contact")}>Contact</a></li>
      </ul>
    </nav>
    <a class="btn btn-primary header-cta" href="{prefix}contact/">Get a Free Quote</a>
    <button class="menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav">
      {icon("menu", "icon-open")}{icon("x", "icon-close")}
    </button>
  </div>
</header>
<nav class="mobile-nav" id="mobile-nav" aria-label="Mobile" aria-hidden="true">
  <a href="{home}">Home</a>
  <span class="sub-label">Services</span>
  <div class="sub">
{mob}
  </div>
  <span class="sub-label">Company</span>
  <a href="{prefix}services/">All Services</a>
  <a href="{prefix}#areas">Service Areas</a>
  <a href="{prefix}#about">About</a>
  <a href="{prefix}contact/">Contact</a>
  <a class="btn btn-primary" href="{prefix}contact/">Get a Free Quote</a>
</nav>
<main id="main">
"""


def footer(prefix):
    svc = "\n".join(f'<li><a href="{prefix}services/{s["slug"]}/">{s["nav"]}</a></li>' for s in SERVICES)
    phone = f'<li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>' if PHONE else ""
    qb_second = (f'<a class="btn btn-outline" href="tel:{PHONE_TEL}">{icon("phone")}Call</a>' if PHONE
                 else f'<a class="btn btn-outline" href="mailto:{EMAIL}">{icon("mail")}Email</a>')
    return f"""</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{prefix}assets/logo.png" alt="{NAME}" width="520" height="{LOGO_H}" loading="lazy">
        <p>Professional residential and commercial cleaning for Vancouver, WA, Portland, OR and the surrounding communities.</p>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
{svc}
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="{prefix}#about">About Us</a></li>
          <li><a href="{prefix}#areas">Service Areas</a></li>
          <li><a href="{prefix}services/">All Services</a></li>
          <li><a href="{prefix}contact/">Request a Quote</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          {phone}
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><span>Vancouver, WA and surrounding areas</span></li>
          <li><span>Portland, OR and surrounding areas</span></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> {NAME}. All rights reserved.</span>
      <span>Serving both sides of the Columbia River.</span>
    </div>
  </div>
</footer>
<div class="quick-bar" aria-label="Quick actions">
  <a class="btn btn-primary" href="{prefix}contact/">Free Quote</a>
  {qb_second}
</div>
<script src="{prefix}js/main.js" defer></script>
</body>
</html>
"""


def service_options(selected=""):
    opts = ['<option value="">Select a service</option>']
    for s in SERVICES:
        sel = " selected" if s["slug"] == selected else ""
        opts.append(f'<option value="{s["slug"]}"{sel}>{s["name"]}</option>')
    opts.append('<option value="not-sure">Not sure yet</option>')
    return "\n".join(opts)


def quote_form(heading="Request a free quote", sub="Tell us a little about your space and we will follow up with a quote, usually within one business day."):
    return f"""<div class="form-card">
  <h3>{heading}</h3>
  <p>{sub}</p>
  <form class="quote-form" novalidate>
    <div class="form-grid">
      <div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="f-location">City or ZIP</label><input id="f-location" name="location" type="text" autocomplete="postal-code" placeholder="e.g. Vancouver 98682"></div>
      <div class="field full"><label for="f-service">Service</label><select id="f-service" name="service">
{service_options()}
      </select></div>
      <div class="field full"><label for="f-message">Tell us about your space</label><textarea id="f-message" name="message" placeholder="Home or office size, number of bedrooms and bathrooms, preferred dates, anything we should know."></textarea></div>
    </div>
    <button class="btn btn-blue" type="submit">Send My Request {icon("arrow")}</button>
    <p class="form-note">No obligation. We never share your information.</p>
    <div class="form-status" role="status" aria-live="polite"></div>
  </form>
</div>"""


def cta_band(prefix, title="Ready for a cleaner space?", text="Tell us about your home or business and get a clear, no-obligation quote from the Ultra Clean PNW team.", service=""):
    q = f"?service={service}" if service else ""
    return f"""<section class="cta-band">
  {img(prefix, "forest", "", lazy=True)}
  <div class="container">
    <span class="eyebrow light">Get started</span>
    <h2>{title}</h2>
    <p>{text}</p>
    <div class="btn-row">
      <a class="btn btn-blue" href="{prefix}contact/{q}">Get a Free Quote {icon("arrow")}</a>
      <a class="btn btn-ghost-light" href="{prefix}services/">Explore Services</a>
    </div>
  </div>
</section>"""


def faq_block(items):
    out = []
    for q, a in items:
        out.append(f"""<details>
  <summary>{escape(q)}<span class="pm">{icon("plus")}</span></summary>
  <div class="answer"><p>{escape(a)}</p></div>
</details>""")
    return '<div class="faq">\n' + "\n".join(out) + "\n</div>"


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def area_served():
    return ([{"@type": "City", "name": f"{c}, WA"} for c in WA_AREAS] +
            [{"@type": "City", "name": f"{c}, OR"} for c in OR_AREAS])


def business_ld():
    d = {
        "@context": "https://schema.org",
        "@type": "HouseCleaningService",
        "@id": SITE + "/#business",
        "name": NAME,
        "url": SITE + "/",
        "logo": SITE + "/assets/logo-large.png",
        "image": SITE + "/assets/og-image.jpg",
        "email": EMAIL,
        "description": "Residential and commercial cleaning serving Vancouver, WA, Portland, OR and the surrounding communities.",
        "address": {"@type": "PostalAddress", "addressLocality": "Vancouver", "addressRegion": "WA", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": 45.6387, "longitude": -122.6615},
        "areaServed": area_served(),
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Cleaning Services",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{SITE}/services/{s['slug']}/"}} for s in SERVICES],
        },
    }
    if PHONE:
        d["telephone"] = PHONE
    return d


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}


def write(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


# ---------------------------------------------------------------- home
def build_home():
    p = ""
    cards = "\n".join(f"""<a class="service-card reveal" href="services/{s['slug']}/">
  <div class="thumb">{img(p, s['img'][0], s['img'][1])}</div>
  <div class="body">
    <h3>{s['name']}</h3>
    <p>{s['card']}</p>
    <span class="text-link">Learn more {icon("arrow")}</span>
  </div>
</a>""" for s in SERVICES)
    wa = "".join(f"<li>{c}</li>" for c in WA_AREAS)
    orr = "".join(f"<li>{c}</li>" for c in OR_AREAS)
    faqs = [
        ("What areas do you serve?", "We serve Vancouver, WA and surrounding Clark County communities like Camas, Washougal, Battle Ground and Ridgefield, plus Portland, OR and nearby cities including Beaverton, Hillsboro, Lake Oswego, Tigard and Gresham. If you are close by and do not see your city listed, reach out and ask."),
        ("How do I get a quote?", "Fill out the quote form or send us an email with your address, the size of your space and the service you need. We will follow up with a clear quote, usually within one business day."),
        ("Do I need to be home during the cleaning?", "No. Many clients provide a door code, lockbox or key. Whatever works best for you, we will make sure your home is secured when we leave."),
        ("Do you bring your own supplies and equipment?", "Yes. Our team arrives with professional supplies and equipment. If you prefer specific products, let us know and we are happy to use them."),
        ("What is the difference between a standard clean and a deep clean?", "A standard clean maintains a home that is already in good shape. A deep clean adds detailed work like baseboards, grout, fixtures, vents and built-up grime. We usually recommend a deep clean for a first visit."),
        ("Do you clean both homes and businesses?", "Yes. We clean houses, apartments, rentals and move-outs, as well as offices and commercial spaces on both sides of the Columbia River."),
    ]
    title = "Ultra Clean PNW | House & Commercial Cleaning in Vancouver, WA & Portland, OR"
    desc = "Ultra Clean PNW provides detailed house cleaning, deep cleaning, move-out, commercial, post-construction and Airbnb cleaning in Vancouver, WA, Portland, OR and surrounding areas. Free quotes."
    website_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE + "/"}
    html = head(p, title, desc, "/", [business_ld(), website_ld, faq_ld(faqs)])
    html += header(p, "home")
    html += f"""
<section class="hero">
  <div class="container hero-grid">
    <div>
      <span class="eyebrow">Vancouver, WA &nbsp;&middot;&nbsp; Portland, OR</span>
      <h1>A cleaner home, <span class="accent">from Vancouver to Portland.</span></h1>
      <p class="lead">Ultra Clean PNW delivers detailed residential and commercial cleaning across the Pacific Northwest. Reliable crews, clear quotes and a clean you notice the moment you walk in.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="contact/">Get a Free Quote {icon("arrow")}</a>
        <a class="btn btn-outline" href="services/">View Services</a>
      </div>
      <ul class="hero-points">
        <li>{icon("check-circle")}Homes, rentals and offices</li>
        <li>{icon("check-circle")}One-time or recurring visits</li>
        <li>{icon("check-circle")}Supplies and equipment included</li>
        <li>{icon("check-circle")}Free, no-obligation quotes</li>
      </ul>
    </div>
    <div class="hero-media">
      <div class="frame">{img(p, "hero-team", "Cleaning team dusting shelves and mopping a living room floor", lazy=False, priority=True)}</div>
      <div class="hero-badge">
        <span class="ico">{icon("mountain")}</span>
        <div><strong>Serving both sides of the Columbia</strong><span>Clark County, WA and the Portland metro</span></div>
      </div>
    </div>
  </div>
</section>

<section class="trust" aria-label="Why clients choose us">
  <div class="container trust-grid">
    <div class="trust-item">{icon("clipboard")}<div><strong>Room-by-room checklists</strong><span>The same standard on every visit</span></div></div>
    <div class="trust-item">{icon("tag")}<div><strong>Clear, upfront quotes</strong><span>No surprises when the job is done</span></div></div>
    <div class="trust-item">{icon("calendar")}<div><strong>Flexible scheduling</strong><span>Weekly, bi-weekly, monthly or one time</span></div></div>
    <div class="trust-item">{icon("pin")}<div><strong>Local to the PNW</strong><span>Vancouver, Portland and nearby cities</span></div></div>
  </div>
</section>

<section class="section" id="services">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow center">Our Services</span>
      <h2>Cleaning services for every kind of space</h2>
      <p class="lead">From weekly house cleaning to post-construction detail work, every service is built around a clear checklist and real attention to detail.</p>
    </div>
    <div class="service-grid">
{cards}
<a class="service-card cta-card reveal" href="contact/">
  <h3>Not sure what you need?</h3>
  <p>Tell us about your space and we will recommend the right service and schedule for your home or business.</p>
  <span class="text-link">Ask for a recommendation {icon("arrow")}</span>
</a>
    </div>
  </div>
</section>

<section class="section alt" id="about">
  <div class="container split">
    <div class="media-stack reveal">
      <div class="main">{img(p, "window-clean", "Cleaner wiping a window in a bright, tidy home")}</div>
      <div class="inset">{img(p, "gloves-wipe", "Gloved hand wiping a surface with spray cleaner")}</div>
    </div>
    <div class="reveal">
      <span class="eyebrow">About Ultra Clean PNW</span>
      <h2>Pacific Northwest cleaning, done with care</h2>
      <p class="lead">Ultra Clean PNW was built on a simple idea: a clean should hold up to a closer look. We serve homeowners, renters, property managers and local businesses on both sides of the Columbia River with the same standard on every visit.</p>
      <ul class="feature-list">
        <li><span class="num">{icon("clipboard")}</span><div><h3>Detail-first checklists</h3><p>Every service follows a written checklist, so baseboards, fixtures and corners get the same attention as the obvious spots.</p></div></li>
        <li><span class="num">{icon("message")}</span><div><h3>Easy, honest communication</h3><p>Clear quotes, reminders before each visit and quick replies when you need to change something.</p></div></li>
        <li><span class="num">{icon("shield")}</span><div><h3>Respect for your space</h3><p>We treat your home or office like our own, from protecting floors and finishes to locking up when we leave.</p></div></li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow center">How It Works</span>
      <h2>Booking a clean is simple</h2>
      <p class="lead">Three quick steps from first message to a spotless space.</p>
    </div>
    <div class="steps">
      <div class="step reveal"><span class="step-num">STEP 01</span><span class="ico">{icon("message")}</span><h3>Request a quote</h3><p>Share a few details about your space, the service you need and your preferred timing.</p></div>
      <div class="step reveal"><span class="step-num">STEP 02</span><span class="ico">{icon("calendar")}</span><h3>Pick your schedule</h3><p>We confirm your price and checklist, then book a time that works for you, one time or recurring.</p></div>
      <div class="step reveal"><span class="step-num">STEP 03</span><span class="ico">{icon("sparkles")}</span><h3>Enjoy the clean</h3><p>Our team arrives prepared, works through every room and leaves your space fresh and ready.</p></div>
    </div>
  </div>
</section>

<section class="areas" id="areas">
  <div class="areas-wrap">
    <figure class="areas-media">
      {img(p, "portland", "Portland skyline and the Fremont Bridge with Mt. St. Helens in the distance")}
      <figcaption>Portland and the Fremont Bridge, with Mt. St. Helens beyond</figcaption>
    </figure>
    <div class="areas-content reveal">
      <span class="eyebrow light">Service Areas</span>
      <h2>Proudly serving Southwest Washington and the Portland metro</h2>
      <p class="lead">Our crews cover Vancouver and Clark County on the Washington side, along with Portland and its surrounding cities in Oregon.</p>
      <div class="area-cols">
        <div class="area-col"><h3>{icon("pin")}Washington</h3><ul>{wa}</ul></div>
        <div class="area-col"><h3>{icon("pin")}Oregon</h3><ul>{orr}</ul></div>
      </div>
      <p class="note">Nearby and not listed? <a href="contact/">Ask us about your area</a>.</p>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow center">FAQ</span>
      <h2>Questions we hear often</h2>
    </div>
    {faq_block(faqs)}
  </div>
</section>

<section class="section" id="quote">
  <div class="container contact-grid">
    <div class="reveal">
      <span class="eyebrow">Free Quote</span>
      <h2>Let's get your space on the schedule</h2>
      <p class="lead">Send a few details and we will reply with a clear quote and available times. No pressure and no obligation.</p>
      <ul class="info-list">
        <li><span class="ico">{icon("mail")}</span><div><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
        <li><span class="ico">{icon("pin")}</span><div><strong>Service area</strong><span>Vancouver, WA, Portland, OR and surrounding communities</span></div></li>
        <li><span class="ico">{icon("clock")}</span><div><strong>Response time</strong><span>Usually within one business day</span></div></li>
      </ul>
    </div>
    <div class="reveal">{quote_form()}</div>
  </div>
</section>
"""
    html += footer(p)
    write("index.html", html)


# ---------------------------------------------------------------- services index
def build_services_index():
    p = "../"
    rows = []
    for i, s in enumerate(SERVICES, 1):
        rows.append(f"""<article class="svc-row reveal">
  <a class="frame" href="{s['slug']}/">{img(p, s['img'][0], s['img'][1])}</a>
  <div>
    <span class="idx">{i:02d}</span>
    <h2>{s['name']}</h2>
    <p class="lead">{s['card']}</p>
    <ul class="checks">{"".join(f'<li>{icon("check")}<span>{it}</span></li>' for it in s["included"][0][2][:3])}</ul>
    <div class="btn-row">
      <a class="btn btn-primary" href="{s['slug']}/">View {s['nav']} {icon("arrow")}</a>
      <a class="btn btn-outline" href="../contact/?service={s['slug']}">Get a Quote</a>
    </div>
  </div>
</article>""")
    title = "Cleaning Services in Vancouver, WA & Portland, OR | Ultra Clean PNW"
    desc = "Explore Ultra Clean PNW cleaning services: residential, deep cleaning, recurring, move-in and move-out, commercial, post-construction and Airbnb cleaning in Vancouver and Portland."
    ld = [crumbs_ld([("Home", "/"), ("Services", "/services/")]),
          {"@context": "https://schema.org", "@type": "ItemList", "name": "Ultra Clean PNW Services",
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/services/{s['slug']}/", "name": s["name"]} for i, s in enumerate(SERVICES)]}]
    html = head(p, title, desc, "/services/", ld)
    html += header(p, "svc-index")
    html += f"""
<section class="page-hero simple">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a>{icon("chev-right")}<span>Services</span></nav>
    <span class="eyebrow">Our Services</span>
    <h1>Cleaning services for homes and businesses</h1>
    <p class="lead">Every Ultra Clean PNW service follows a detailed checklist and is tailored to your space. Choose a service below to see exactly what is included.</p>
  </div>
</section>
<section class="section">
  <div class="container svc-rows">
{chr(10).join(rows)}
  </div>
</section>
{cta_band(p)}
"""
    html += footer(p)
    write("services/index.html", html)


# ---------------------------------------------------------------- service detail
def build_service(s):
    p = "../../"
    idx = SERVICES.index(s)
    others = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
    included = "\n".join(f"""<div class="inc-card reveal">
  <h3><span class="ico">{icon(ic)}</span>{t}</h3>
  <ul class="checks">{"".join(f'<li>{icon("check")}<span>{it}</span></li>' for it in items)}</ul>
</div>""" for t, ic, items in s["included"])
    gallery = "\n".join(f"<figure>{img(p, n, a)}</figure>" for n, a in s["gallery"])
    related = "\n".join(f"""<a href="../{o['slug']}/">{img(p, o['img'][0], o['img'][1])}<div><strong>{o['name']}</strong><span>Learn more</span></div></a>""" for o in others)
    ideal = "".join(f"<li>{icon('check')}{x}</li>" for x in s["ideal"])
    path = f"/services/{s['slug']}/"
    service_ld = {
        "@context": "https://schema.org", "@type": "Service",
        "name": s["name"], "serviceType": s["name"], "description": s["desc"],
        "url": SITE + path, "image": f"{SITE}/assets/img/{s['img'][0]}.jpg",
        "provider": {"@type": "HouseCleaningService", "@id": SITE + "/#business", "name": NAME, "url": SITE + "/"},
        "areaServed": area_served(),
    }
    ld = [service_ld, crumbs_ld([("Home", "/"), ("Services", "/services/"), (s["name"], path)]), faq_ld(s["faqs"])]
    html = head(p, s["title"], s["desc"], path, ld)
    html += header(p, s["slug"])
    html += f"""
<section class="page-hero">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../../">Home</a>{icon("chev-right")}<a href="../">Services</a>{icon("chev-right")}<span>{s['name']}</span></nav>
    <div class="split">
      <div>
        <span class="eyebrow">{s['name']}</span>
        <h1>{s['h1']}</h1>
        <p class="lead">{s['intro']}</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="../../contact/?service={s['slug']}">Get a Free Quote {icon("arrow")}</a>
          <a class="btn btn-outline" href="#included">What's Included</a>
        </div>
      </div>
      <div class="frame">{img(p, s['img'][0], s['img'][1], lazy=False, priority=True)}</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container detail-grid">
    <div class="prose reveal">
      <span class="eyebrow">Overview</span>
      <h2>What to expect</h2>
      {"".join(f"<p>{x}</p>" for x in s['overview'])}
      <h3 style="margin-top:28px">Ideal for</h3>
      <ul class="ideal">{ideal}</ul>
    </div>
    <aside class="sticky reveal">
      <div class="aside-card">
        <h3>Get your free quote</h3>
        <p>Share a few details and we will send a clear price and available times.</p>
        <ul>
          <li>{icon("check")}Free, no-obligation quote</li>
          <li>{icon("check")}Supplies and equipment included</li>
          <li>{icon("check")}Serving Vancouver and Portland</li>
        </ul>
        <a class="btn btn-blue" href="../../contact/?service={s['slug']}">Request a Quote {icon("arrow")}</a>
      </div>
    </aside>
  </div>
</section>

<section class="section alt" id="included">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow center">What's Included</span>
      <h2>Your {s['name'].lower().replace('airbnb', 'Airbnb')} checklist</h2>
      <p class="lead">A clear look at what our team takes care of. Have special requests? Add them to your quote request.</p>
    </div>
    <div class="included cols-3">
{included}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="gallery reveal">
{gallery}
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow center">FAQ</span>
      <h2>{s['name']} questions</h2>
    </div>
    {faq_block(s['faqs'])}
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head left reveal">
      <span class="eyebrow">More Services</span>
      <h2>You might also need</h2>
    </div>
    <div class="related">
{related}
    </div>
  </div>
</section>
{cta_band(p, service=s['slug'])}
"""
    html += footer(p)
    write(f"services/{s['slug']}/index.html", html)


# ---------------------------------------------------------------- contact
def build_contact():
    p = "../"
    title = "Contact Ultra Clean PNW | Free Cleaning Quote in Vancouver & Portland"
    desc = "Request a free cleaning quote from Ultra Clean PNW. Serving Vancouver, WA, Portland, OR and surrounding areas with residential and commercial cleaning."
    ld = [crumbs_ld([("Home", "/"), ("Contact", "/contact/")]),
          {"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact Ultra Clean PNW", "url": SITE + "/contact/",
           "about": {"@id": SITE + "/#business"}}]
    phone = (f'<li><span class="ico">{icon("phone")}</span><div><strong>Phone</strong><a href="tel:{PHONE_TEL}">{PHONE}</a></div></li>' if PHONE else "")
    html = head(p, title, desc, "/contact/", ld)
    html += header(p, "contact")
    html += f"""
<section class="page-hero simple">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a>{icon("chev-right")}<span>Contact</span></nav>
    <span class="eyebrow">Contact</span>
    <h1>Request your free quote</h1>
    <p class="lead">Tell us about your home or business and the service you need. We will reply with a clear quote and available times, usually within one business day.</p>
  </div>
</section>
<section class="section">
  <div class="container contact-grid">
    <div>
      <h2>Get in touch</h2>
      <p class="muted">Prefer email? Write to us directly and include your address, the size of your space and the service you are interested in.</p>
      <ul class="info-list">
        {phone}
        <li><span class="ico">{icon("mail")}</span><div><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
        <li><span class="ico">{icon("pin")}</span><div><strong>Washington</strong><span>Vancouver, Camas, Washougal, Battle Ground, Ridgefield and nearby</span></div></li>
        <li><span class="ico">{icon("pin")}</span><div><strong>Oregon</strong><span>Portland, Beaverton, Hillsboro, Lake Oswego, Tigard, Gresham and nearby</span></div></li>
        <li><span class="ico">{icon("clock")}</span><div><strong>Response time</strong><span>Usually within one business day</span></div></li>
      </ul>
      <div class="media-stack" style="margin-top:40px;padding-bottom:0">
        <div class="main">{img(p, "pnw-home", "Pacific Northwest home with a clean front porch")}</div>
      </div>
    </div>
    <div>{quote_form()}</div>
  </div>
</section>
"""
    html += footer(p)
    write("contact/index.html", html)


# ---------------------------------------------------------------- 404
def build_404():
    p = "/"
    html = head(p, "Page Not Found | Ultra Clean PNW", "The page you are looking for could not be found.", "/404", [])
    html = html.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    html += header(p)
    html += f"""
<section class="not-found">
  <div class="container">
    <div class="code">404</div>
    <h1>We could not find that page</h1>
    <p class="lead" style="margin:0 auto 28px">The page may have moved. Head back home or browse our cleaning services.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn-primary" href="/">Back to Home</a>
      <a class="btn btn-outline" href="/services/">View Services</a>
    </div>
  </div>
</section>
"""
    html += footer(p)
    write("404.html", html)


# ---------------------------------------------------------------- seo files
def build_seo_files(date="2026-10-20"):
    urls = ["/", "/services/", "/contact/"] + [f"/services/{s['slug']}/" for s in SERVICES]
    pr = {"/": "1.0", "/services/": "0.9", "/contact/": "0.7"}
    items = "\n".join(f"""  <url>
    <loc>{SITE}{u}</loc>
    <lastmod>{date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{pr.get(u, '0.8')}</priority>
  </url>""" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /_src/\n\nSitemap: {SITE}/sitemap.xml\n")
    write("site.webmanifest", json.dumps({
        "name": NAME, "short_name": "Ultra Clean", "start_url": "/", "display": "standalone",
        "background_color": "#ffffff", "theme_color": THEME,
        "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}],
    }, indent=2) + "\n")


if __name__ == "__main__":
    with Image.open(os.path.join(ROOT, "assets", "logo.png")) as _l:
        LOGO_H = round(_l.height * 520 / _l.width)
    PHONE_TEL = "+1" + "".join(ch for ch in PHONE if ch.isdigit())[-10:] if PHONE else ""
    build_home()
    build_services_index()
    for s in SERVICES:
        build_service(s)
    build_contact()
    build_404()
    build_seo_files()
    print("Built", 4 + len(SERVICES), "pages")

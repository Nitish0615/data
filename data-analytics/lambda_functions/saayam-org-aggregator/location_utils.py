# location_utils.py

def get_beneficiary_coordinates(request_id, beneficiary_id):
    """
    Priority:
    1. requests.req_loc
    2. user_locations.curr_loc
    3. users + cities + states + countries → geocode
    4. unknown
    """

    # ---- Priority 1: request coordinates ----
    req_loc = get_request_location(request_id)
    if req_loc:
        return {
            "lat": req_loc["latitude"],
            "lon": req_loc["longitude"],
            "source": "request_location",
        }

    # ---- Priority 2: user_locations.curr_loc ----
    curr_loc = get_user_current_location(beneficiary_id)
    if curr_loc:
        return {
            "lat": curr_loc["latitude"],
            "lon": curr_loc["longitude"],
            "source": "user_current_location",
        }

    # ---- Priority 3: profile address → geocode ----
    address = get_beneficiary_address(beneficiary_id)
    if address:
        coords = geocode_address(address)
        if coords:
            return {
                "lat": coords["lat"],
                "lon": coords["lon"],
                "source": "profile_address_geocoded",
            }

    # ---- Priority 4: unknown ----
    return {
        "lat": None,
        "lon": None,
        "source": "unknown",
    }


def get_request_location(request_id):
    """
    Fetch req_loc from virginia_dev_saayam_rdbms.requests.
    req_loc is expected to be a JSON field containing:
    {
        "latitude": ...,
        "longitude": ...
    }
    """

    try:
        conn = psycopg2.connect(
            host="YOUR_DB_HOST",
            database="virginia_dev_saayam_rdbms",
            user="YOUR_DB_USER",
            password="YOUR_DB_PASSWORD"
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = """
            SELECT req_loc
            FROM requests
            WHERE id = %s
        """

        cur.execute(query, (request_id,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row and row["req_loc"]:
            req_loc = row["req_loc"]
            return {
                "latitude": req_loc.get("latitude"),
                "longitude": req_loc.get("longitude")
            }

        return None

    except Exception as e:
        print("Error fetching request location:", e)
        return None


def get_user_current_location(user_id):
    """
    Query virginia_dev_saayam_rdbms.user_locations.curr_loc.
    For now, mock: no current location.
    """
    return None


def get_beneficiary_address(user_id):
    """
    Build address from users + cities + states + countries.
    For now, mock.
    """
    if user_id == 123:
        return "Mountain View, CA 94043, United States"
    return None


def geocode_address(address):
    """
    Geocoding stub.
    DO NOT hard-code provider; just a placeholder.
    """
    # Example: pretend Mountain View, CA
    return {
        "lat": 37.4220,
        "lon": -122.0841,
    }


def get_org_coordinates(org):
    """
    Resolve organization coordinates.

    - If org is online-only → status 'online'
    - Else:
        - build address
        - (later) check cache
        - geocode address
    """

    # Online-only org
    if org.get("Org-type") == "online":
        return {
            "lat": None,
            "lon": None,
            "status": "online",
        }

    address = build_org_address(org)
    if not address:
        return {
            "lat": None,
            "lon": None,
            "status": "unknown_location",
        }

    # TODO: check cache here (DB table) in real implementation
    coords = geocode_address(address)
    if not coords:
        return {
            "lat": None,
            "lon": None,
            "status": "not_found",
        }

    # TODO: save to cache in real implementation
    return {
        "lat": coords["lat"],
        "lon": coords["lon"],
        "status": "ok",
    }


def build_org_address(org):
    """
    Build full org address from DB fields or GenAI response.
    For now, use 'location' field.
    """
    return org.get("location")

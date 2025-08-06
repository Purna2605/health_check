def get_hospital_map_url(location):
    """
    Returns a Google Maps search URL for hospitals near the given location.
    """
    if not location:
        location = "India"
    
    # Clean the location string and replace spaces with plus signs for URL
    clean_location = location.strip().replace(' ', '+')
    query = f"https://www.google.com/maps/search/hospitals+near+{clean_location}"
    return query
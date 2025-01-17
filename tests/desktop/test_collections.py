# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import time
import uuid


from pages.desktop.home import Home
from pages.desktop.details import Details


class TestCollections:

    @pytest.mark.native
    @pytest.mark.nondestructive
    def test_featured_tab_is_highlighted_by_default(self, base_url, selenium):
        home_page = Home(base_url, selenium)
        featured_collections_page = home_page.header.site_navigation_menu("Collections").click()
        assert 'Featured' == featured_collections_page.default_selected_tab

    def test_create_and_delete_collection(self, base_url, selenium, logged_in):
        home_page = Home(base_url, selenium)
        collections_page = home_page.header.site_navigation_menu('Collections').click()
        create_collection_page = collections_page.click_create_collection_button()

        collection_uuid = uuid.uuid4().hex
        collection_time = repr(time.time())
        collection_name = collection_uuid[:30 - len(collection_time):] + collection_time

        create_collection_page.type_name(collection_name)
        create_collection_page.type_description(collection_name)
        collection = create_collection_page.click_create_collection()

        assert 'Collection created!' == collection.notification
        assert collection_name == collection.collection_name
        collection.delete()
        user_collections = collection.delete_confirmation()
        assert user_collections.has_no_results

    @pytest.mark.native
    def test_user_my_collections_page(self, base_url, selenium, logged_in, user):
        home_page = Home(base_url, selenium)
        my_collections_page = home_page.header.click_my_collections()
        assert 'Collections by %s :: Add-ons for Firefox' % user['display_name'] == my_collections_page.page_title
        assert 'Collections by %s' % user['display_name'] == my_collections_page.my_collections_header_text

    @pytest.mark.native
    def test_user_my_favorites_page(self, base_url, selenium, logged_in):
        details_page = Details(base_url, selenium, 'Firebug')
        details_page.click_add_to_favorites()
        assert details_page.is_addon_marked_as_favorite

        home_page = Home(base_url, selenium)
        my_favorites_page = home_page.header.click_my_favorites()
        assert my_favorites_page.is_the_current_page
        assert 'My Favorite Add-ons' == my_favorites_page.my_favorites_header_text

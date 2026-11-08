package cgeo.geocaching.settings;

import cgeo.geocaching.CgeoApplication;
import cgeo.geocaching.R;
import cgeo.geocaching.settings.fragments.PreferenceServiceOpencachingFragment;

import android.content.res.Resources;
import android.content.res.XmlResourceParser;

import java.io.IOException;
import java.util.ArrayList;
import java.util.EnumSet;
import java.util.List;
import java.util.Set;

import org.apache.commons.lang3.Strings;
import org.junit.Test;
import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;
import static org.assertj.core.api.Assertions.assertThat;

public class OCPreferenceKeysTest {

    /**
     * The opencaching site of the settings screen is derived from the key of the clicked services list entry
     * (see SettingsActivity.onPreferenceStartFragment), so each such entry must map to a site.
     */
    @Test
    public void testServicesListEntriesResolveToSite() throws Exception {
        final List<String> keys = getOpencachingServiceEntryKeys();
        assertThat(keys).isNotEmpty();
        for (final String key : keys) {
            assertThat(OCPreferenceKeys.getByAuthPrefKey(key)).as("site for services entry '%s'", key).isNotNull();
        }
    }

    @Test
    public void testEverySiteHasServicesListEntry() throws Exception {
        final Set<OCPreferenceKeys> sites = EnumSet.noneOf(OCPreferenceKeys.class);
        for (final String key : getOpencachingServiceEntryKeys()) {
            sites.add(OCPreferenceKeys.getByAuthPrefKey(key));
        }
        assertThat(sites).containsExactlyInAnyOrder(OCPreferenceKeys.values());
    }

    @Test
    public void testPrefScreenKeyResolvesToSite() {
        final Resources res = CgeoApplication.getInstance().getResources();
        for (final OCPreferenceKeys site : OCPreferenceKeys.values()) {
            assertThat(OCPreferenceKeys.getByPrefScreenKey(res.getString(site.prefScreenId))).isEqualTo(site);
        }
    }

    /**
     * keys of all entries in the services list which open the opencaching settings screen
     */
    private static List<String> getOpencachingServiceEntryKeys() throws XmlPullParserException, IOException {
        final Resources res = CgeoApplication.getInstance().getResources();
        final List<String> keys = new ArrayList<>();
        try (XmlResourceParser parser = res.getXml(R.xml.preferences_services)) {
            while (parser.next() != XmlPullParser.END_DOCUMENT) {
                if (parser.getEventType() != XmlPullParser.START_TAG) {
                    continue;
                }
                String key = null;
                String fragment = null;
                for (int i = 0; i < parser.getAttributeCount(); i++) {
                    if ("key".equals(parser.getAttributeName(i))) {
                        final int keyId = parser.getAttributeResourceValue(i, 0);
                        key = keyId != 0 ? res.getString(keyId) : parser.getAttributeValue(i);
                    } else if ("fragment".equals(parser.getAttributeName(i))) {
                        fragment = parser.getAttributeValue(i);
                    }
                }
                if (Strings.CS.equals(fragment, PreferenceServiceOpencachingFragment.class.getName())) {
                    keys.add(key);
                }
            }
        }
        return keys;
    }
}

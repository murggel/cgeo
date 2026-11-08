package cgeo.geocaching.settings.fragments;

import cgeo.geocaching.settings.AbstractAuthorizationPreference;
import cgeo.geocaching.settings.OCPreferenceKeys;
import cgeo.geocaching.utils.PreferenceUtils;
import cgeo.geocaching.utils.ShareUtils;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.preference.Preference;
import androidx.preference.PreferenceFragmentCompat;

import org.apache.commons.lang3.Strings;

/**
 * Settings screen for all opencaching based services. The site is given by its siteId as fragment argument.
 */
public class PreferenceServiceOpencachingFragment extends PreferenceFragmentCompat {

    /** Has to match the "extra" entries in preferences_services.xml. */
    public static final String ARG_SITE_ID = "ocSiteId";

    public static PreferenceServiceOpencachingFragment newInstance(@NonNull final OCPreferenceKeys site) {
        final PreferenceServiceOpencachingFragment fragment = new PreferenceServiceOpencachingFragment();
        final Bundle args = new Bundle();
        args.putString(ARG_SITE_ID, site.siteId);
        fragment.setArguments(args);
        return fragment;
    }

    @NonNull
    private OCPreferenceKeys getSite() {
        final String siteId = requireArguments().getString(ARG_SITE_ID);
        final OCPreferenceKeys site = OCPreferenceKeys.getBySiteId(siteId);
        if (site == null) {
            throw new IllegalStateException("Unknown opencaching site: " + siteId);
        }
        return site;
    }

    @Override
    public void onCreatePreferences(final Bundle savedInstanceState, final String rootKey) {
        final OCPreferenceKeys site = getSite();
        setPreferencesFromResource(site.preferencesXmlId, rootKey);

        // Open website Preference
        final Preference openWebsite = findPreference(getString(site.websitePrefId));
        final String urlOrHost = site.authParams.host;
        PreferenceUtils.setOnPreferenceClickListener(openWebsite, preference -> {
            final String url = Strings.CS.startsWith(urlOrHost, "http") ? urlOrHost : "http://" + urlOrHost;
            ShareUtils.openUrl(getContext(), url);
            return true;
        });
    }

    @Override
    public void onResume() {
        super.onResume();
        final OCPreferenceKeys site = getSite();
        requireActivity().setTitle(site.titleId);

        // Update authentication preference
        AbstractAuthorizationPreference.updateAuthorizationPreference(this, site.authPrefId);
    }
}

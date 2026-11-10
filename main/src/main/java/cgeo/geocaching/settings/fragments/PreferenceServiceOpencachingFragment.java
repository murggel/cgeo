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
 * Settings screen for all opencaching based services. The site is given as fragment argument,
 * either by {@link #newInstance} or by an {@code <extra android:name="ocSite">} of the opening preference.
 */
public class PreferenceServiceOpencachingFragment extends PreferenceFragmentCompat {

    // must match the extra name used in preferences_services.xml
    private static final String ARG_SITE = "ocSite";

    public static PreferenceServiceOpencachingFragment newInstance(@NonNull final OCPreferenceKeys site) {
        final PreferenceServiceOpencachingFragment fragment = new PreferenceServiceOpencachingFragment();
        final Bundle args = new Bundle();
        putSite(args, site);
        fragment.setArguments(args);
        return fragment;
    }

    private static void putSite(@NonNull final Bundle args, @NonNull final OCPreferenceKeys site) {
        args.putString(ARG_SITE, site.name());
    }

    @NonNull
    private OCPreferenceKeys getSite() {
        final String site = requireArguments().getString(ARG_SITE);
        if (site == null) {
            throw new IllegalStateException("No opencaching site given");
        }
        return OCPreferenceKeys.valueOf(site);
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

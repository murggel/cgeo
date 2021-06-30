package cgeo.geocaching.settings;

import android.os.Bundle;

import androidx.preference.PreferenceFragmentCompat;

import cgeo.geocaching.R;


public class SettingsBasicPreferencesFragment extends PreferenceFragmentCompat {

    @Override
    public void onCreatePreferences(Bundle savedInstanceState, String rootKey) {
        // Load the preferences from an XML resource
        setPreferencesFromResource(R.xml.pref_basic, rootKey);
    }
}

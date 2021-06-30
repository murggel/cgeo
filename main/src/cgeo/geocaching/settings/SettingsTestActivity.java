package cgeo.geocaching.settings;

import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
import androidx.preference.PreferenceFragmentCompat;

import cgeo.geocaching.R;

public class SettingsTestActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        // Display the fragment as the main content.
        getSupportFragmentManager()
          .beginTransaction()
          .replace(R.id.preferences, new SettingsTestFragment())
         .commit();
    }
}

package cgeo.geocaching.settings;

import cgeo.geocaching.R;
import cgeo.geocaching.ui.dialog.Dialogs;
import cgeo.geocaching.utils.LocalizationUtils;
import cgeo.geocaching.utils.Log;

import android.content.Context;
import android.util.AttributeSet;
import android.view.View;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.preference.Preference;
import androidx.preference.PreferenceFragmentCompat;
import androidx.preference.PreferenceViewHolder;

import org.apache.commons.lang3.StringUtils;

// https://www.joehxblog.com/how-to-add-a-long-click-to-an-androidx-preference/
public abstract class AbstractAuthorizationPreference extends Preference {

    private final SettingsActivity activity;

    private final View.OnLongClickListener longClickListener = v -> {
        if (!isAuthorized()) {
            return false;
        }

        final AlertDialog.Builder builder = Dialogs.newBuilder(v.getContext());
        builder.setMessage(R.string.auth_forget_message)
                .setIcon(android.R.drawable.ic_dialog_alert)
                .setTitle(R.string.auth_forget_title)
                .setPositiveButton(android.R.string.yes, (dialog, id) -> {
                    revokeAuthorization();
                    updateAuthorizationInfo();
                })
                .setNegativeButton(android.R.string.cancel, (dialog, id) -> dialog.cancel());
        builder.create().show();

        return true;
    };

    AbstractAuthorizationPreference(final Context context, final AttributeSet attrs) {
        super(context, attrs);
        activity = (SettingsActivity) context;
    }

    AbstractAuthorizationPreference(final Context context, final AttributeSet attrs, final int defStyle) {
        super(context, attrs, defStyle);
        activity = (SettingsActivity) context;
    }

    public static void updateAuthorizationPreference(final PreferenceFragmentCompat preferenceFragment, final int prefKeyId) {
        final String prefKey = LocalizationUtils.getPlainString(prefKeyId);
        final Preference preference = preferenceFragment.findPreference(prefKey);
        if (!(preference instanceof AbstractAuthorizationPreference)) {
            Log.e("No authorization preference found for key " + prefKey + " in " + preferenceFragment.getClass().getSimpleName());
            return;
        }
        ((AbstractAuthorizationPreference) preference).updateAuthorizationInfo();
    }

    @Override
    public void onBindViewHolder(@NonNull final PreferenceViewHolder holder) {
        super.onBindViewHolder(holder);

        setOnPreferenceClickListener(getOnPreferenceClickListener(activity));

        final View itemView = holder.itemView;
        itemView.setOnLongClickListener(this.longClickListener);
    }

    void updateAuthorizationInfo() {
        if (isAuthorized()) {
            final String userName = getUserName();
            setTitle(R.string.settings_reauthorize);
            // user name is only known after a successful login
            setSummary(StringUtils.isNotBlank(userName) ? LocalizationUtils.getString(R.string.auth_connected_as, userName) : LocalizationUtils.getString(R.string.auth_connected));
            setIcon(null);
        } else {
            setTitle(R.string.settings_authorize);
            setSummary(R.string.auth_unconnected_tap_here);
            setIcon(R.drawable.attribute_firstaid);
        }
    }

    protected abstract OnPreferenceClickListener getOnPreferenceClickListener(SettingsActivity settingsActivity);

    protected boolean isAuthorized() {
        return false;
    }

    protected void revokeAuthorization() {
    }

    @Nullable
    protected String getUserName() {
        return null;
    }
}

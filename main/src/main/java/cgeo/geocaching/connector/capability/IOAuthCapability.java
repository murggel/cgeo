package cgeo.geocaching.connector.capability;

import cgeo.geocaching.connector.IConnector;

/**
 * connector capability for providing public and secret OAuth tokens
 */
public interface IOAuthCapability extends IConnector {
    int getTokenPublicPrefKeyId();

    int getTokenSecretPrefKeyId();

    /**
     * Drops cached login data (user name, finds, login status), e.g. after the OAuth tokens
     * have been changed by a new authorization or a revoke. The next login retrieves them again.
     */
    default void resetLoginStatus() {
        // nothing cached by default
    }
}

package cgeo.geocaching.filters.core;

import cgeo.geocaching.models.Geocache;
import cgeo.geocaching.storage.DataStore;


public class TrackableCountFilter extends NumberRangeGeocacheFilter<Float> {

    public TrackableCountFilter() {
        super(Float::valueOf, f -> f);
    }

    @Override
    public Float getValue(final Geocache cache) {
        return (float) cache.getTrackableCount();
    }

    @Override
    protected String getSqlColumnName() {
        return DataStore.dbFieldCaches_inventoryunknown;
    }
}

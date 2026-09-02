package cgeo.geocaching.command;

import cgeo.geocaching.R;
import cgeo.geocaching.models.CacheArtefactParser;
import cgeo.geocaching.models.CacheVariableList;
import cgeo.geocaching.models.Geocache;
import cgeo.geocaching.models.Waypoint;
import cgeo.geocaching.utils.LocalizationUtils;

import android.app.Activity;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.lang3.StringUtils;
import org.apache.commons.lang3.Strings;


public class PersonalNoteStoreWaypointsCommand extends AbstractCommand {

    @NonNull
    private final Collection<Geocache> caches;
    private final Map<String, String> personalNotes = new HashMap<>();
    private int updatedCount = 0;

    public PersonalNoteStoreWaypointsCommand(@NonNull final Activity context, @NonNull final Collection<Geocache> caches) {
        super(context, R.string.command_personal_note_store_waypoints_progress);
        this.caches = caches;
    }

    @Override
    protected void doCommand() {
        updatedCount = 0;
        for (final Geocache cache : caches) {
            final String oldPersonalNote = cache.getPersonalNote();
            final List<Waypoint> userModifiedWaypoints = cache.getWaypoints().stream().filter(Waypoint::isUserModified).toList();
            final CacheVariableList variablesList = cache.getVariables();
            if (!userModifiedWaypoints.isEmpty() || !variablesList.isEmpty()) {
                final String newNote = CacheArtefactParser.putParseableWaypointsInText(oldPersonalNote, userModifiedWaypoints, variablesList);
                final String updatedPersonalNote = StringUtils.trimToEmpty(newNote);
                if (!Strings.CI.equals(StringUtils.trimToEmpty(oldPersonalNote), updatedPersonalNote)) {
                    personalNotes.put(cache.getGeocode(), oldPersonalNote);
                    cache.setPersonalNote(updatedPersonalNote);
                    updatedCount++;
                }
            }
        }
    }


    @Override
    protected void undoCommand() {
        for (final Geocache cache : caches) {
            final String oldPersonalNote = personalNotes.get(cache.getGeocode());
            cache.setPersonalNote(oldPersonalNote);
        }
    }


    @Override
    protected void onFinished() {
        // nothing to do
    }

    @Override
    @Nullable
    protected String getResultMessage() {
        return LocalizationUtils.getString(R.string.command_personal_note_store_waypoints_result, updatedCount);
    }
}

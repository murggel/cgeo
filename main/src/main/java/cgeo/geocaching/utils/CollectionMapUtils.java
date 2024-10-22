package cgeo.geocaching.utils;


import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class CollectionMapUtils {

    private CollectionMapUtils() {
        // utility class
    }

    public static <K, V extends Comparable<? super V>> Map<K, V> sortByValue(final Map<K, V> map) {
        final List<Map.Entry<K, V>> list = new ArrayList<>(map.entrySet());
        list.sort(Map.Entry.comparingByValue());

        final Map<K, V> result = new LinkedHashMap<>();
        for (Map.Entry<K, V> entry : list) {
            result.put(entry.getKey(), entry.getValue());
        }

        return result;
    }

    public static <K, V extends Comparable<? super V>> List<K> getListOfKeys(final Map<K, V> map) {
        final List<K> listOfKeys = new ArrayList<>();
        final Iterator<Map.Entry<K, V>> it = map.entrySet().iterator();
        while (it.hasNext()) {
            final Map.Entry<K, V> entry = it.next();
            listOfKeys.add(entry.getKey());
        }

        return listOfKeys;
    }
}

import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  SafeAreaView,
  StyleSheet,
  Text,
  View,
} from "react-native";

export default function HistoryTab() {
  const [historyData, setHistoryData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Replace this block with your actual API endpoint call
    const fetchScanHistory = async () => {
      try {
        setIsLoading(true);
        // const response = await fetch('YOUR_API_URL/scans');
        // const data = await response.json();
        // setHistoryData(data);

        // Simulating empty response state initialization for placeholder validation
        setHistoryData([]);
      } catch (error) {
        console.error("Error retrieving scan historical data: ", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchScanHistory();
  }, []);

  const renderItem = ({ item }) => {
    const isInProgress = item.status === "In Progress";

    return (
      <View style={styles.historyItem}>
        <View style={styles.metaColumn}>
          <Text style={styles.historyDate}>
            {new Date(item.date).toLocaleDateString("en-US", {
              month: "short",
              day: "numeric",
              year: "numeric",
            })}
          </Text>
          <View
            style={[
              styles.statusBadge,
              isInProgress ? styles.badgeProgress : styles.badgeComplete,
            ]}
          >
            <Text
              style={[
                styles.statusText,
                isInProgress ? styles.textProgress : styles.textComplete,
              ]}
            >
              {item.status}
            </Text>
          </View>
        </View>
        <Text
          style={[styles.historyScore, isInProgress && styles.scorePending]}
        >
          {isInProgress ? "--" : `${item.score}%`}
        </Text>
      </View>
    );
  };

  // Render loading feedback placeholder during API handshake
  if (isLoading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.centeredState}>
          <ActivityIndicator size="large" color="#FF4D6D" />
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.appBar}>
        <Text style={styles.brandTag}>TIMELINE</Text>
        <Text style={styles.title}>Scan History</Text>
      </View>

      <FlatList
        data={historyData}
        renderItem={renderItem}
        keyExtractor={(item) => item.id || item._id}
        contentContainerStyle={styles.list}
        showsVerticalScrollIndicator={false}
        ListEmptyComponent={
          <View style={styles.emptyStateContainer}>
            <View style={styles.emptyDotContainer}>
              <View style={styles.emptyDot} />
            </View>
            <Text style={styles.emptyHeading}>No scans logged yet</Text>
            <Text style={styles.emptySubheading}>
              Your completed AI reports will appear organized right here.
            </Text>
          </View>
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFF8F9", // Unified off-white pink identity
  },
  appBar: {
    paddingHorizontal: 20,
    paddingTop: 24,
    marginBottom: 16,
  },
  brandTag: {
    fontSize: 11,
    fontWeight: "700",
    color: "#FF4D6D",
    letterSpacing: 2,
    marginBottom: 4,
  },
  title: {
    fontSize: 28,
    fontWeight: "800",
    color: "#2B2D42",
    letterSpacing: -0.5,
  },
  list: {
    paddingHorizontal: 20,
    paddingBottom: 32,
    gap: 12,
  },
  historyItem: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    padding: 18,
    borderRadius: 24,
    shadowColor: "#FF7597",
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.04,
    shadowRadius: 16,
    elevation: 3,
  },
  metaColumn: {
    alignItems: "flex-start",
    gap: 6,
  },
  historyDate: {
    fontSize: 15,
    fontWeight: "700",
    color: "#2B2D42",
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  badgeComplete: {
    backgroundColor: "#FFF0F3",
  },
  badgeProgress: {
    backgroundColor: "#FFFBEB",
  },
  statusText: {
    fontSize: 11,
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: 0.3,
  },
  textComplete: {
    color: "#FF4D6D",
  },
  textProgress: {
    color: "#D97706",
  },
  historyScore: {
    fontSize: 20,
    fontWeight: "800",
    color: "#2B2D42",
    letterSpacing: -0.5,
  },
  scorePending: {
    color: "#8D99AE",
  },
  centeredState: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  /* Empty State UI elements */
  emptyStateContainer: {
    alignItems: "center",
    justifyContent: "center",
    marginTop: 80,
    paddingHorizontal: 32,
  },
  emptyDotContainer: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: "#FFFFFF",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 16,
    shadowColor: "#FF7597",
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.05,
    shadowRadius: 12,
    elevation: 2,
  },
  emptyDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: "#FFD3DC",
  },
  emptyHeading: {
    fontSize: 16,
    fontWeight: "700",
    color: "#2B2D42",
    textAlign: "center",
    marginBottom: 6,
  },
  emptySubheading: {
    fontSize: 13,
    color: "#8D99AE",
    textAlign: "center",
    lineHeight: 18,
    fontWeight: "500",
  },
});

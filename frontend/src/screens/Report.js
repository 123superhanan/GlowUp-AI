import {
  SafeAreaView,
  ScrollView,
  Share,
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

export default function Report({ route, navigation }) {
  const data = route?.params?.analysis || {
    skin: "Normal",
    bodyType: "Ectomorph",
    confidence: 0.92,
  };

  const share = async () => {
    await Share.share({ message: "My GlowUp AI Analysis Report!" });
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#FFF8F9" />

      <ScrollView
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Header App Bar Section */}
        <View style={styles.appBar}>
          <Text style={styles.brandTag}>ANALYSIS COMPLETED</Text>
          <Text style={styles.title}>Your Report</Text>
        </View>

        {/* 1. Results Metrics Card */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Metrics Summary</Text>

          <View style={styles.row}>
            <Text style={styles.label}>Skin Classification</Text>
            <Text style={styles.value}>{data.skin}</Text>
          </View>

          <View style={styles.row}>
            <Text style={styles.label}>Body Architecture</Text>
            <Text style={styles.value}>{data.bodyType}</Text>
          </View>

          <View style={styles.row}>
            <Text style={styles.label}>AI Confidence Score</Text>
            <View style={styles.badge}>
              <Text style={styles.badgeText}>
                {(data.confidence * 100).toFixed(0)}%
              </Text>
            </View>
          </View>
        </View>

        {/* 2. Recommendations Card */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Action Plan</Text>

          <View style={styles.listItem}>
            <View style={styles.bulletPoint} />
            <Text style={styles.rec}>
              High protein nutrition strategy (1.6g/kg)
            </Text>
          </View>

          <View style={styles.listItem}>
            <View style={styles.bulletPoint} />
            <Text style={styles.rec}>
              Structured strength training (3x weekly)
            </Text>
          </View>

          <View style={styles.listItem}>
            <View style={styles.bulletPoint} />
            <Text style={styles.rec}>
              Daily barrier optimization (Moisturizer + SPF)
            </Text>
          </View>
        </View>

        {/* 3. Products Card */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Recommended Regimen</Text>

          <View style={styles.productRow}>
            <View style={styles.productInfo}>
              <Text style={styles.productName}>CeraVe Cleanser</Text>
              <Text style={styles.productCategory}>Daily Essentials</Text>
            </View>
            <Text style={styles.productPrice}>$15.99</Text>
          </View>

          <View style={styles.productRow}>
            <View style={styles.productInfo}>
              <Text style={styles.productName}>Neutrogena Moisturizer</Text>
              <Text style={styles.productCategory}>Hydration Layer</Text>
            </View>
            <Text style={styles.productPrice}>$12.99</Text>
          </View>
        </View>

        {/* 4. Double Floating Action Buttons */}
        <View style={styles.rowBtns}>
          <TouchableOpacity
            style={styles.btnSecondary}
            onPress={() => navigation.navigate("MainTabs")}
            activeOpacity={0.8}
          >
            <Text style={styles.btnTextSecondary}>New Scan</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.btnPrimary}
            onPress={share}
            activeOpacity={0.9}
          >
            <Text style={styles.btnTextPrimary}>Share Insights</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFF8F9", // Uniform rich off-white pink app background canvas
  },
  content: {
    paddingHorizontal: 20,
    paddingTop: 24,
    paddingBottom: 40,
  },
  appBar: {
    alignItems: "center",
    marginBottom: 24,
  },
  brandTag: {
    fontSize: 11,
    fontWeight: "700",
    color: "#FF4D6D",
    letterSpacing: 2,
    marginBottom: 6,
  },
  title: {
    fontSize: 28,
    fontWeight: "800",
    color: "#2B2D42",
    letterSpacing: -0.5,
  },
  card: {
    backgroundColor: "#FFFFFF",
    padding: 20,
    borderRadius: 24,
    marginBottom: 16,
    shadowColor: "#FF7597",
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.06,
    shadowRadius: 16,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: "700",
    color: "#2B2D42",
    marginBottom: 16,
    letterSpacing: -0.2,
  },
  /* Table Rows */
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#FFF0F3",
  },
  label: {
    fontSize: 14,
    color: "#8D99AE",
    fontWeight: "500",
  },
  value: {
    fontWeight: "600",
    color: "#2B2D42",
    fontSize: 14,
  },
  badge: {
    backgroundColor: "#FFF0F3",
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  badgeText: {
    color: "#FF4D6D",
    fontWeight: "700",
    fontSize: 13,
  },
  /* Recommendation Items */
  listItem: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 8,
  },
  bulletPoint: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: "#FF7597",
    marginRight: 12,
  },
  rec: {
    fontSize: 14,
    color: "#4A4E69",
    fontWeight: "500",
    flex: 1,
  },
  /* Product Section Items */
  productRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 10,
  },
  productInfo: {
    flex: 1,
  },
  productName: {
    fontSize: 14,
    fontWeight: "600",
    color: "#2B2D42",
  },
  productCategory: {
    fontSize: 11,
    color: "#8D99AE",
    marginTop: 2,
    fontWeight: "500",
  },
  productPrice: {
    fontSize: 14,
    fontWeight: "700",
    color: "#FF4D6D",
  },
  /* Button Footer Section */
  rowBtns: {
    flexDirection: "row",
    gap: 12,
    marginTop: 8,
  },
  btnPrimary: {
    flex: 2,
    backgroundColor: "#FF4D6D",
    paddingVertical: 16,
    borderRadius: 16,
    alignItems: "center",
    justifyContent: "center",
    shadowColor: "#FF4D6D",
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.2,
    shadowRadius: 12,
    elevation: 3,
  },
  btnSecondary: {
    flex: 1,
    backgroundColor: "#FFFFFF",
    paddingVertical: 16,
    borderRadius: 16,
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
    borderColor: "#FFD3DC",
  },
  btnTextPrimary: {
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: 15,
  },
  btnTextSecondary: {
    color: "#FF4D6D",
    fontWeight: "700",
    fontSize: 15,
  },
});

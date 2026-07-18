import { useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Image,
  SafeAreaView,
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

export default function PhotoUpload({ navigation }) {
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const selectImage = () => {
    setImage({ uri: "https://via.placeholder.com/300" });
  };

  const analyze = () => {
    if (!image) {
      Alert.alert(
        "Photo Required",
        "Please select a photo to begin your AI analysis.",
      );
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      navigation.navigate("Report", {
        analysis: { skin: "Normal", bodyType: "Ectomorph", confidence: 0.92 },
      });
    }, 2000);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#FFF8F9" />

      <View style={styles.content}>
        {/* Header App Bar Section */}
        <View style={styles.appBar}>
          <Text style={styles.title}>AI Scanner</Text>
          <Text style={styles.subtitle}>
            Upload a clear portrait to begin analysis
          </Text>
        </View>

        {/* Tactile Camera Viewport Container */}
        <View style={styles.viewportCard}>
          {image ? (
            <View style={styles.imageWrapper}>
              <Image source={{ uri: image.uri }} style={styles.previewImage} />
              <TouchableOpacity
                style={styles.retakeBadge}
                onPress={selectImage}
                activeOpacity={0.9}
              >
                <Text style={styles.retakeText}>Replace</Text>
              </TouchableOpacity>
            </View>
          ) : (
            <TouchableOpacity
              style={styles.uploadTrigger}
              onPress={selectImage}
              activeOpacity={0.8}
            >
              {/* Corner brackets to look like a camera focus framing device */}
              <View style={[styles.corner, styles.topLeft]} />
              <View style={[styles.corner, styles.topRight]} />
              <View style={[styles.corner, styles.bottomLeft]} />
              <View style={[styles.corner, styles.bottomRight]} />

              <View style={styles.innerUploadCircle}>
                <Text style={styles.uploadIconText}>+</Text>
              </View>
              <Text style={styles.uploadActionText}>Select From Gallery</Text>
              <Text style={styles.uploadHintText}>JPEG, PNG up to 10MB</Text>
            </TouchableOpacity>
          )}
        </View>

        {/* Floating Action Button Bar */}
        <View style={styles.actionSection}>
          <TouchableOpacity
            style={[styles.primaryButton, !image && styles.buttonDisabled]}
            onPress={analyze}
            disabled={!image || loading}
            activeOpacity={0.9}
          >
            {loading ? (
              <ActivityIndicator color="#FFFFFF" size="small" />
            ) : (
              <Text style={styles.primaryButtonText}>Start Analysis</Text>
            )}
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFF8F9", // Premium, rich off-white pink tint app canvas
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
    justifyContent: "space-between",
    paddingBottom: 20,
  },
  appBar: {
    marginTop: 24,
    alignItems: "center",
  },
  title: {
    fontSize: 24,
    fontWeight: "700",
    color: "#2B2D42",
    letterSpacing: -0.3,
  },
  subtitle: {
    fontSize: 14,
    color: "#8D99AE",
    marginTop: 6,
    fontWeight: "500",
  },
  viewportCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 24,
    height: "55%",
    width: "100%",
    shadowColor: "#FF7597",
    shadowOffset: { width: 0, height: 12 },
    shadowOpacity: 0.12,
    shadowRadius: 24,
    elevation: 8,
    overflow: "hidden",
    padding: 16,
  },
  uploadTrigger: {
    flex: 1,
    backgroundColor: "#FFF0F3",
    borderRadius: 16,
    justifyContent: "center",
    alignItems: "center",
    position: "relative",
  },
  innerUploadCircle: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: "#FFFFFF",
    justifyContent: "center",
    alignItems: "center",
    shadowColor: "#FF7597",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 2,
    marginBottom: 16,
  },
  uploadIconText: {
    fontSize: 28,
    color: "#FF4D6D",
    fontWeight: "300",
    marginTop: -2,
  },
  uploadActionText: {
    color: "#2B2D42",
    fontWeight: "600",
    fontSize: 16,
  },
  uploadHintText: {
    color: "#FF7597",
    fontSize: 12,
    marginTop: 6,
    fontWeight: "500",
  },
  imageWrapper: {
    flex: 1,
    position: "relative",
  },
  previewImage: {
    width: "100%",
    height: "100%",
    borderRadius: 16,
    backgroundColor: "#F8F9FA",
  },
  retakeBadge: {
    position: "absolute",
    bottom: 16,
    right: 16,
    backgroundColor: "rgba(255, 255, 255, 0.95)",
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 20,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 6,
    elevation: 3,
  },
  retakeText: {
    color: "#FF4D6D",
    fontWeight: "600",
    fontSize: 13,
  },
  actionSection: {
    width: "100%",
    marginBottom: 16,
  },
  primaryButton: {
    backgroundColor: "#FF4D6D", // Rich vibrant app action color
    paddingVertical: 18,
    borderRadius: 18,
    alignItems: "center",
    justifyContent: "center",
    shadowColor: "#FF4D6D",
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.25,
    shadowRadius: 16,
    elevation: 4,
  },
  primaryButtonText: {
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: 16,
    letterSpacing: 0.2,
  },
  buttonDisabled: {
    backgroundColor: "#FFCCD5",
    shadowOpacity: 0,
    elevation: 0,
  },
  /* Scanner Box Camera Targets Corner Styles */
  corner: {
    position: "absolute",
    width: 16,
    height: 16,
    borderColor: "#FF7597",
  },
  topLeft: { top: 20, left: 20, borderTopWidth: 2, borderLeftWidth: 2 },
  topRight: { top: 20, right: 20, borderTopWidth: 2, borderRightWidth: 2 },
  bottomLeft: {
    bottom: 20,
    left: 20,
    borderBottomWidth: 2,
    borderLeftWidth: 2,
  },
  bottomRight: {
    bottom: 20,
    right: 20,
    borderBottomWidth: 2,
    borderRightWidth: 2,
  },
});

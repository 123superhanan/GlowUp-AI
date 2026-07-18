import { useState } from "react";
import {
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";

export default function GlowUpDashboard({ navigation }) {
  const [chatText, setChatText] = useState("");
  const [messages, setMessages] = useState([]);

  const quickPrompts = [
    "Best hairstyle for my face shape?",
    "What skincare routine do I need?",
    "How can I improve my beard growth?",
    "What glasses suit me?",
    "Best colors for my skin tone?",
  ];

  const handlePromptPress = (prompt) => {
    setChatText(prompt);
    // Auto-send after a short delay
    setTimeout(() => {
      handleSend(prompt);
    }, 300);
  };

  const handleSend = (text) => {
    const message = text || chatText;
    if (!message.trim()) return;

    // Add user message
    setMessages((prev) => [
      ...prev,
      { id: Date.now(), type: "user", text: message },
    ]);
    setChatText("");

    // Simulate AI response
    setTimeout(() => {
      const responses = [
        "Based on your Oval face shape and Warm Olive skin tone, I'd recommend a textured crop with a side part. It adds volume and defines your jawline.",
        "For your skin type, I recommend a gentle cleanser, vitamin C serum in the morning, and retinol at night. Always finish with SPF 50!",
        "To improve beard growth, try using beard oil daily, exfoliate your skin twice a week, and consider biotin supplements.",
        "Rectangular or square glasses would complement your face shape perfectly. Go for dark frames to create contrast.",
        "With your Warm Olive skin tone, earth tones like olive green, terracotta, and navy blue will look amazing on you.",
      ];

      const randomResponse =
        responses[Math.floor(Math.random() * responses.length)];

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          type: "ai",
          text: randomResponse,
        },
      ]);
    }, 1000);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#FFF8F9" />

      {/* Header */}
      <View style={styles.appBar}>
        <TouchableOpacity style={styles.iconButton} activeOpacity={0.7}>
          <View style={styles.menuIconContainer}>
            <View style={styles.menuLine} />
            <View style={[styles.menuLine, { width: 14 }]} />
            <View style={styles.menuLine} />
          </View>
        </TouchableOpacity>

        <Text style={styles.brandText}>GlowUp AI</Text>

        <TouchableOpacity
          style={styles.profileButton}
          activeOpacity={0.7}
          onPress={() => navigation?.navigate("Settings")}
        >
          <View style={styles.profileAvatarMock} />
        </TouchableOpacity>
      </View>

      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={styles.keyboardView}
        keyboardVerticalOffset={Platform.OS === "ios" ? 90 : 0}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
          ref={(ref) => {
            if (ref) {
              setTimeout(() => {
                ref.scrollToEnd({ animated: true });
              }, 100);
            }
          }}
        >
          {/* Messages */}
          {messages.length > 0 ? (
            <View style={styles.messagesContainer}>
              {messages.map((msg) => (
                <View
                  key={msg.id}
                  style={[
                    styles.messageWrapper,
                    msg.type === "user" ? styles.userWrapper : styles.aiWrapper,
                  ]}
                >
                  <View
                    style={[
                      styles.messageBubble,
                      msg.type === "user" ? styles.userBubble : styles.aiBubble,
                    ]}
                  >
                    <Text
                      style={[
                        styles.messageText,
                        msg.type === "user" ? styles.userText : styles.aiText,
                      ]}
                    >
                      {msg.text}
                    </Text>
                  </View>
                </View>
              ))}
            </View>
          ) : (
            <>
              {/* Hero Card - Only show if no messages */}
              <View style={styles.heroCard}>
                <Text style={styles.heroTitle}>✨ GlowUp AI</Text>
                <Text style={styles.heroSubtitle}>
                  Upload your photo to start your personalized transformation
                  journey.
                </Text>

                <TouchableOpacity
                  style={styles.uploadBox}
                  activeOpacity={0.8}
                  onPress={() => navigation?.navigate("PhotoUpload")}
                >
                  <View style={styles.uploadIconCircle}>
                    <Text style={styles.uploadPlus}>+</Text>
                  </View>
                  <Text style={styles.uploadText}>Upload Your Photo</Text>
                  <Text style={styles.uploadSubtext}>
                    Analyze face shape, skin tone & more
                  </Text>
                </TouchableOpacity>
              </View>

              {/* Quick Prompts */}
              <View style={styles.suggestionSection}>
                <Text style={styles.suggestionHeader}>Ask a question:</Text>

                {quickPrompts.map((item, index) => (
                  <TouchableOpacity
                    key={index}
                    style={styles.promptChip}
                    onPress={() => handlePromptPress(item)}
                    activeOpacity={0.7}
                  >
                    <View style={styles.chipBullet} />
                    <Text style={styles.promptText}>{item}</Text>
                  </TouchableOpacity>
                ))}
              </View>
            </>
          )}
        </ScrollView>

        {/* Input Bar */}
        <View style={styles.inputWrapper}>
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.textInput}
              placeholder="Ask GlowUp anything..."
              placeholderTextColor="#B8B8B8"
              value={chatText}
              onChangeText={setChatText}
              onSubmitEditing={() => handleSend()}
              returnKeyType="send"
            />
            <TouchableOpacity
              style={[
                styles.sendButton,
                !chatText.trim() && styles.sendDisabled,
              ]}
              disabled={!chatText.trim()}
              activeOpacity={0.8}
              onPress={() => handleSend()}
            >
              <Text style={styles.sendIconText}>↑</Text>
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFF8F9",
  },
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingTop: 16,
    paddingBottom: 100,
  },
  /* Header */
  appBar: {
    height: 60,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: "#F0F0F0",
    backgroundColor: "#FFF8F9",
  },
  brandText: {
    fontSize: 18,
    fontWeight: "800",
    color: "#2B2D42",
    letterSpacing: -0.3,
  },
  menuIconContainer: {
    width: 24,
    height: 16,
    justifyContent: "space-between",
  },
  menuLine: {
    width: 20,
    height: 2.5,
    backgroundColor: "#2B2D42",
    borderRadius: 2,
  },
  profileButton: {
    justifyContent: "center",
    alignItems: "center",
  },
  profileAvatarMock: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: "#FF4D6D",
    borderWidth: 2,
    borderColor: "#FFF0F3",
  },
  /* Hero Card */
  heroCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 24,
    padding: 24,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.05,
    shadowRadius: 16,
    elevation: 4,
    marginBottom: 24,
  },
  heroTitle: {
    fontSize: 28,
    fontWeight: "800",
    color: "#2B2D42",
    marginBottom: 8,
  },
  heroSubtitle: {
    fontSize: 14,
    color: "#8D99AE",
    textAlign: "center",
    lineHeight: 20,
    marginBottom: 24,
    paddingHorizontal: 10,
  },
  uploadBox: {
    backgroundColor: "#FFF0F3",
    borderColor: "#FFCCD5",
    borderWidth: 2,
    borderStyle: "dashed",
    borderRadius: 16,
    width: "100%",
    paddingVertical: 32,
    alignItems: "center",
    justifyContent: "center",
  },
  uploadIconCircle: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: "#FFFFFF",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 12,
    shadowColor: "#FF4D6D",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
  },
  uploadPlus: {
    fontSize: 24,
    color: "#FF4D6D",
    fontWeight: "300",
    marginTop: -2,
  },
  uploadText: {
    fontSize: 16,
    fontWeight: "700",
    color: "#2B2D42",
    marginBottom: 4,
  },
  uploadSubtext: {
    fontSize: 12,
    color: "#8D99AE",
    fontWeight: "500",
  },
  /* Suggestion */
  suggestionSection: {
    width: "100%",
    paddingHorizontal: 4,
  },
  suggestionHeader: {
    fontSize: 14,
    fontWeight: "700",
    color: "#2B2D42",
    marginBottom: 12,
    letterSpacing: 0.2,
  },
  promptChip: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    paddingVertical: 14,
    paddingHorizontal: 16,
    borderRadius: 14,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: "#F0F0F0",
  },
  chipBullet: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: "#FF4D6D",
    marginRight: 12,
  },
  promptText: {
    fontSize: 14,
    fontWeight: "500",
    color: "#2B2D42",
  },
  /* Messages */
  messagesContainer: {
    paddingBottom: 16,
  },
  messageWrapper: {
    marginBottom: 12,
  },
  userWrapper: {
    alignItems: "flex-end",
  },
  aiWrapper: {
    alignItems: "flex-start",
  },
  messageBubble: {
    maxWidth: "85%",
    padding: 14,
    borderRadius: 18,
  },
  userBubble: {
    backgroundColor: "#FF4D6D",
    borderBottomRightRadius: 4,
  },
  aiBubble: {
    backgroundColor: "#FFFFFF",
    borderBottomLeftRadius: 4,
    borderWidth: 1,
    borderColor: "#F0F0F0",
  },
  messageText: {
    fontSize: 15,
    lineHeight: 22,
  },
  userText: {
    color: "#FFFFFF",
  },
  aiText: {
    color: "#2B2D42",
  },
  /* Input */
  inputWrapper: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: "#FFF8F9",
    paddingHorizontal: 20,
    paddingBottom: Platform.OS === "ios" ? 24 : 16,
    paddingTop: 8,
  },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    borderRadius: 24,
    borderWidth: 1,
    borderColor: "#E8E8E8",
    paddingHorizontal: 16,
    height: 56,
  },
  textInput: {
    flex: 1,
    height: "100%",
    color: "#2B2D42",
    fontSize: 15,
    fontWeight: "500",
    paddingRight: 10,
  },
  sendButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: "#FF4D6D",
    alignItems: "center",
    justifyContent: "center",
  },
  sendDisabled: {
    backgroundColor: "#E8E8E8",
  },
  sendIconText: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "700",
    marginTop: -2,
  },
});

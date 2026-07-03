import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet, SafeAreaView, Alert, ActivityIndicator } from 'react-native';

export default function PhotoUpload({ navigation }) {
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);

  // Simulate image upload (remove this and add your own logic)
  const selectImage = () => {
    // For demo: use a placeholder image
    setImage({ uri: 'https://via.placeholder.com/300' });
  };

  const analyze = () => {
    if (!image) { 
      Alert.alert('Error', 'Select an image first'); 
      return; 
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      navigation.navigate('Report', { 
        analysis: { skin: 'Normal', bodyType: 'Ectomorph', confidence: 0.92 } 
      });
    }, 2000);
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>📸 Upload Photo</Text>

        {image ? (
          <Image source={{ uri: image.uri }} style={styles.image} />
        ) : (
          <View style={styles.placeholder}>
            <Text style={styles.placeholderIcon}>📷</Text>
            <Text>No photo selected</Text>
          </View>
        )}

        <TouchableOpacity style={[styles.btn, styles.btnOutline]} onPress={selectImage}>
          <Text style={styles.btnOutlineText}>📁 Select Image</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.btn, styles.btnPrimary, !image && styles.disabled]} 
          onPress={analyze} 
          disabled={!image || loading}
        >
          {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.btnText}>✨ Analyze</Text>}
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    backgroundColor: '#f8f9fa' 
  },
  content: { 
    flex: 1, 
    padding: 24, 
    justifyContent: 'center' 
  },
  title: { 
    fontSize: 32, 
    fontWeight: 'bold', 
    textAlign: 'center', 
    marginBottom: 20 
  },
  image: { 
    width: 300, 
    height: 300, 
    borderRadius: 20, 
    alignSelf: 'center', 
    marginBottom: 20 
  },
  placeholder: { 
    width: 300, 
    height: 300, 
    borderRadius: 20, 
    backgroundColor: '#e9ecef', 
    justifyContent: 'center', 
    alignItems: 'center', 
    alignSelf: 'center', 
    marginBottom: 20 
  },
  placeholderIcon: { 
    fontSize: 60 
  },
  btn: { 
    padding: 16, 
    borderRadius: 12, 
    alignItems: 'center',
    marginBottom: 12 
  },
  btnPrimary: { 
    backgroundColor: '#6C63FF' 
  },
  btnOutline: { 
    backgroundColor: 'transparent', 
    borderWidth: 1, 
    borderColor: '#6C63FF' 
  },
  btnOutlineText: { 
    color: '#6C63FF', 
    fontWeight: '600' 
  },
  btnText: { 
    color: '#fff', 
    fontWeight: '600' 
  },
  disabled: { 
    opacity: 0.5 
  },
});
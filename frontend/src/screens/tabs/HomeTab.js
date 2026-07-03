import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

export default function HomeTab({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>✨ GlowUp AI</Text>
      <Text style={styles.subtitle}>Your transformation journey starts here</Text>
      
      <TouchableOpacity 
        style={styles.button}
        onPress={() => navigation.navigate('PhotoUpload')}
      >
        <Text style={styles.buttonText}>Start Analysis →</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#f8f9fa',
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#2d3436',
  },
  subtitle: {
    fontSize: 18,
    color: '#636e72',
    marginTop: 10,
    marginBottom: 40,
  },
  button: {
    backgroundColor: '#6C63FF',
    paddingHorizontal: 40,
    paddingVertical: 16,
    borderRadius: 30,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});

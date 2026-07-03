import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, SafeAreaView, ScrollView, Share } from 'react-native';

export default function Report({ route, navigation }) {
  const data = route?.params?.analysis || { skin: 'Normal', bodyType: 'Ectomorph', confidence: 0.92 };

  const share = async () => {
    await Share.share({ message: '✨ My GlowUp AI Report!' });
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.emoji}>✨</Text>
        <Text style={styles.title}>Your Report</Text>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>📊 Results</Text>
          <View style={styles.row}><Text>Skin</Text><Text style={styles.value}>{data.skin}</Text></View>
          <View style={styles.row}><Text>Body Type</Text><Text style={styles.value}>{data.bodyType}</Text></View>
          <View style={styles.row}><Text>Confidence</Text><Text style={styles.value}>{(data.confidence * 100).toFixed(0)}%</Text></View>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>💪 Recommendations</Text>
          <Text style={styles.rec}>🥗 High protein diet (1.6g/kg)</Text>
          <Text style={styles.rec}>🏋️ 3x/week strength training</Text>
          <Text style={styles.rec}>🧴 Daily moisturizer + SPF</Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>🛍️ Products</Text>
          <Text style={styles.rec}>🛒 CeraVe Cleanser - $15.99</Text>
          <Text style={styles.rec}>🛒 Neutrogena Moisturizer - $12.99</Text>
        </View>

        <View style={styles.rowBtns}>
          <TouchableOpacity style={styles.btn} onPress={share}>
            <Text style={styles.btnText}>📤 Share</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.btn, styles.btnSecondary]} onPress={() => navigation.navigate('Onboarding')}>
            <Text style={styles.btnTextSecondary}>🔄 Start Over</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8f9fa' },
  content: { padding: 20, paddingBottom: 40 },
  emoji: { fontSize: 48, textAlign: 'center', marginVertical: 10 },
  title: { fontSize: 32, fontWeight: 'bold', textAlign: 'center', marginBottom: 20 },
  card: { backgroundColor: '#fff', padding: 20, borderRadius: 16, marginBottom: 16 },
  cardTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 12 },
  row: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: '#f1f2f6' },
  value: { fontWeight: '600' },
  rec: { paddingVertical: 8, fontSize: 16 },
  rowBtns: { flexDirection: 'row', gap: 12, marginTop: 8 },
  btn: { flex: 1, backgroundColor: '#6C63FF', padding: 16, borderRadius: 12, alignItems: 'center' },
  btnSecondary: { backgroundColor: '#e9ecef' },
  btnText: { color: '#fff', fontWeight: '600' },
  btnTextSecondary: { color: '#2d3436', fontWeight: '600' },
});
import React from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';

const historyData = [
  { id: '1', date: '2026-07-03', status: 'Completed', score: 85 },
  { id: '2', date: '2026-07-02', status: 'In Progress', score: 70 },
  { id: '3', date: '2026-07-01', status: 'Completed', score: 90 },
  { id: '4', date: '2026-06-30', status: 'Completed', score: 78 },
];

export default function HistoryTab() {
  const renderItem = ({ item }) => (
    <View style={styles.historyItem}>
      <View>
        <Text style={styles.historyDate}>{item.date}</Text>
        <Text style={styles.historyStatus}>{item.status}</Text>
      </View>
      <Text style={styles.historyScore}>{item.score}%</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>📊 History</Text>
      <FlatList
        data={historyData}
        renderItem={renderItem}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f8f9fa',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2d3436',
    marginBottom: 20,
  },
  list: {
    gap: 12,
  },
  historyItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  historyDate: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2d3436',
  },
  historyStatus: {
    fontSize: 14,
    color: '#636e72',
    marginTop: 4,
  },
  historyScore: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#6C63FF',
  },
});

import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet, Alert, SafeAreaView } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';

type Secret = { name: string; value: string; date: string };
type Question = { id: string; prompt: string; options: string[]; hint?: string };

const QUESTIONS: Question[] = [
  { id: 'target', prompt: 'Cible principale ?', options: ['Commerçantes ivoiriennes', 'Infospreneurs', 'Micro-entreprises', 'Autre'], hint: 'Choisis ta cible primaire' },
  { id: 'product', prompt: 'Produit phare ?', options: ['Friendises afrodisiaques', 'SaaS-MCP', 'AAAIAA MCP', 'RAG MCP'], hint: 'Le cœur du revenue' },
  { id: 'revenue', prompt: 'Modèle revenue ?', options: ['Abonnement', 'Commission', 'Abo+Commission', 'Autre'], hint: 'Récurrent ou ponctuel' },
  { id: 'team', prompt: 'Équipe ?', options: ['Solo + bot', 'Team infographiste', 'Team vidéo/motion', 'Agentic.sh'], hint: 'Qui fait quoi' },
  { id: 'priority', prompt: 'Priorité ?', options: ['SSH → Déploiement', 'Pro upgrade', 'Spots Blender', 'Contenu'], hint: 'Urgence du moment' },
];

export default function App() {
  const [secrets, setSecrets] = useState<Secret[]>([]);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [maieutic, setMaieutic] = useState('');

  useEffect(() => { loadSecrets(); }, []);

  const loadSecrets = async () => {
    const stored = await AsyncStorage.getItem('eon10_secrets');
    if (stored) setSecrets(JSON.parse(stored));
  };

  const saveSecret = async (name: string, value: string) => {
    await SecureStore.setItemAsync(`eon10_${name}`, value);
    const updated = [...secrets.filter(s => s.name !== name), { name, value, date: new Date().toISOString() }];
    setSecrets(updated);
    await AsyncStorage.setItem('eon10_secrets', JSON.stringify(updated));
    Alert.alert('🔒', `${name} sauvegardé chiffré.`);
  };

  const answerQ = (opt: string) => {
    const q = QUESTIONS[currentQ];
    const newAnswers = { ...answers, [q.id]: opt };
    setAnswers(newAnswers);

    // Maieutic suggestion
    const suggestions: Record<string, string> = {
      target: 'Commerçantes ivoiriennes = friendises récurrentes. Cible B2B retail Abidjan.',
      product: 'Friendises = moteur revenue. SaaS-MCP = outil interne. Pas confondre.',
      revenue: 'Abo+Commission = double source. Abo stable, commission scalabile.',
      team: 'Solo + bot = lean. Team = plus rapide mais coût fixe.',
      priority: 'SSH débloqué = déploiement immédiat des 10 tâches.',
    };
    setMaieutic(suggestions[opt] || 'Bonne réponse.');

    if (currentQ < QUESTIONS.length - 1) {
      setCurrentQ(currentQ + 1);
    } else {
      const summary = Object.entries(newAnswers).map(([k, v]) => `${k}: ${v}`).join('\n');
      Alert.alert('✅ Profil EON10', summary + '\n\n' + maieutic);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>EON10 Secrets 🔒</Text>

        {/* Secrets form */}
        <Text style={styles.section}>Coller un secret ci-dessous :</Text>
        <SecretForm onSave={saveSecret} />

        {/* Saved secrets list */}
        <Text style={styles.section}>Secrets sauvegardés :</Text>
        {secrets.map(s => (
          <View key={s.name} style={styles.secretCard}>
            <Text style={styles.secretName}>{s.name}</Text>
            <Text style={styles.secretMask}>{'*'.repeat(Math.min(s.value.length, 8))}...</Text>
            <Text style={styles.secretDate}>{new Date(s.date).toLocaleDateString('fr-FR')}</Text>
          </View>
        ))}

        {/* QCM Maieutique */}
        <Text style={styles.section}>Maïeutique EON10 :</Text>
        {currentQ < QUESTIONS.length && (
          <View style={styles.qcm}>
            <Text style={styles.qPrompt}>{QUESTIONS[currentQ].prompt}</Text>
            {QUESTIONS[currentQ].hint && <Text style={styles.hint}>{QUESTIONS[currentQ].hint}</Text>}
            {QUESTIONS[currentQ].options.map(opt => (
              <TouchableOpacity key={opt} style={styles.option} onPress={() => answerQ(opt)}>
                <Text style={styles.optionText}>{opt}</Text>
              </TouchableOpacity>
            ))}
          </View>
        )}

        {maieutic ? <Text style={styles.maieutic}>{maieutic}</Text> : null}
      </ScrollView>
    </SafeAreaView>
  );
}

function SecretForm({ onSave }: { onSave: (name: string, value: string) => void }) {
  const [name, setName] = useState('');
  const [value, setValue] = useState('');
  return (
    <View style={styles.form}>
      <TextInput style={styles.input} placeholder="Nom (ex: EXPLABS_API_KEY)" value={name} onChangeText={setName} autoCapitalize="none" />
      <TextInput style={styles.input} placeholder="Colle le secret ici" value={value} onChangeText={setValue} secureTextEntry />
      <TouchableOpacity style={styles.button} onPress={() => { if (name && value) onSave(name, value); setValue(''); }}>
        <Text style={styles.buttonText}>🔒 Sauvegarder</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0a0a0a' },
  content: { padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#00ff88', marginBottom: 20 },
  section: { fontSize: 16, color: '#888', marginTop: 16, marginBottom: 8 },
  form: { gap: 8 },
  input: { backgroundColor: '#1a1a1a', color: '#fff', padding: 12, borderRadius: 8, borderWidth: 1, borderColor: '#333' },
  button: { backgroundColor: '#00ff88', padding: 12, borderRadius: 8, alignItems: 'center', marginTop: 8 },
  buttonText: { color: '#000', fontWeight: 'bold' },
  secretCard: { backgroundColor: '#1a1a1a', padding: 12, borderRadius: 8, marginTop: 6, borderLeftWidth: 3, borderLeftColor: '#00ff88' },
  secretName: { color: '#00ff88', fontWeight: 'bold' },
  secretMask: { color: '#666', marginTop: 4 },
  secretDate: { color: '#444', marginTop: 2, fontSize: 11 },
  qcm: { backgroundColor: '#1a1a1a', padding: 16, borderRadius: 12, marginTop: 8 },
  qPrompt: { color: '#fff', fontSize: 16, fontWeight: 'bold', marginBottom: 8 },
  hint: { color: '#888', fontSize: 12, marginBottom: 8 },
  option: { backgroundColor: '#222', padding: 12, borderRadius: 8, marginTop: 6 },
  optionText: { color: '#00ff88' },
  maieutic: { backgroundColor: '#1a2a1a', padding: 12, borderRadius: 8, marginTop: 12, color: '#aaa', fontStyle: 'italic' },
});

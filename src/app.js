const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const port = 3000;

app.use(express.json());
app.use(cors());

// Route principale pour les prédictions Big Five
app.post('/personality', async (req, res) => {
  try {
    const response = await axios.post('https://04fd-34-106-229-103.ngrok-free.app/predict', req.body);
    
    const result = {
      extraversion: response.data.extraversion,
      stabilite_emotionnelle: response.data.stabilite_emotionnelle,
      agreabilite: response.data.agreabilite, 
      conscience: response.data.conscience,
      ouverture: response.data.ouverture
    };

    res.json(result);
  } catch (error) {
    res.status(500).json({ 
      error: "Erreur lors de la prédiction",
      details: error.message 
    });
  }
});

app.listen(port, () => {
  console.log(`Serveur démarré sur le port ${port}`);
}); 
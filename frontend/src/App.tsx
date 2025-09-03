import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Chip,
  CircularProgress,
  Container,
  IconButton,
  Stack,
  TextField,
  Typography,
  Button,
  Tooltip,
  Snackbar,
  Alert,
  Divider,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import SaveIcon from "@mui/icons-material/Save";
import CloseIcon from "@mui/icons-material/Close";
import AddIcon from "@mui/icons-material/Add";

/**
 * Frontend Keyword Manager for the Expenses Bot
 * -------------------------------------------------
 * • React + TypeScript + Material UI
 * • Lists categories from the backend and lets you edit their keywords
 * • Keywords are comma‑separated; keywords may contain spaces; commas split tokens
 * • Optimistic UI with diff‑based sync (POST new keywords, DELETE removed keywords)
 * • Minimal dependency on runtime env via API_BASE_URL (from window.ENV or fallback)
 *
 * Back‑end API (from README):
 * - GET    /categories
 * - GET    /categories/{category_id}/keywords
 * - POST   /categories/{category_id}/keywords   body: { "keyword": string }
 * - DELETE /categories/{category_id}/keywords   body: { "keyword": string }
 */

// ===== Utilities
const API_BASE_URL = (window as any)?.ENV?.API_BASE_URL || import.meta.env?.VITE_API_BASE_URL || "http://backend:8000";

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${path}`;
  const options = {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
    ...init,
  };
  console.log('API Request:', url, options);
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${text}`);
  }
  return res.json();
}


// Normalize a keyword for equality checks (trim + collapse spaces + lowercase)
function norm(s: string) {
  return s.trim().replace(/\s+/g, " ").toLowerCase();
}

function uniqueKeepOrder(values: string[]) {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const v of values) {
    const k = norm(v);
    if (!k || seen.has(k)) continue;
    seen.add(k);
    out.push(v.trim().replace(/\s+/g, " "));
  }
  return out;
}

// Tokenize an input string by commas, preserving spaces within each token
function tokenizeByComma(input: string): string[] {
  return input
    .split(",")
    .map((t) => t)
    .map((t) => t.trim())
    .filter((t) => t.length > 0);
}

// ===== Types
interface Category {
  id: number;
  name: string;
  emoji?: string;
}

// ===== Editable Keywords Component
function EditableKeywords({ categoryId }: { categoryId: number }) {
  const [loading, setLoading] = useState(true);
  const [keywords, setKeywords] = useState<string[]>([]); // display (possibly edited)
  const [original, setOriginal] = useState<string[]>([]); // last loaded from server
  const [editing, setEditing] = useState(false);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    api<string[]>(`/categories/${categoryId}/keywords`)
      .then((list) => {
        if (cancelled) return;
        const cleaned = uniqueKeepOrder(list);
        setKeywords(cleaned);
        setOriginal(cleaned);
      })
      .catch((e) => setError(e.message))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [categoryId]);

  function handleAddTokens(raw: string) {
    const tokens = tokenizeByComma(raw);
    if (!tokens.length) return;
    setKeywords((prev) => uniqueKeepOrder([...prev, ...tokens]));
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === ",") {
      e.preventDefault();
      const value = (e.target as HTMLInputElement).value;
      if (value.trim()) {
        handleAddTokens(value);
        setInput("");
      }
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (input.trim()) {
        handleAddTokens(input);
        setInput("");
      }
    } else if (e.key === "Backspace" && input.length === 0 && keywords.length > 0) {
      // convenience: backspace with empty input removes the last chip
      setKeywords((prev) => prev.slice(0, -1));
    }
  }

  function handleBlur() {
    if (input.trim()) {
      handleAddTokens(input);
      setInput("");
    }
  }

  function removeChip(idx: number) {
    setKeywords((prev) => prev.filter((_, i) => i !== idx));
  }

  const diff = useMemo(() => {
    const oSet = new Set(original.map(norm));
    const kSet = new Set(keywords.map(norm));

    const additions = keywords.filter((k) => !oSet.has(norm(k)));
    const removals = original.filter((k) => !kSet.has(norm(k)));
    const changed = additions.length > 0 || removals.length > 0;
    return { additions, removals, changed };
  }, [keywords, original]);

  async function saveChanges() {
    setBusy(true);
    setError(null);
    try {
      // Apply removals first, then additions
      for (const kw of diff.removals) {
        await api(`/categories/${categoryId}/keywords`, {
          method: "DELETE",
          body: JSON.stringify({ keyword: kw }),
        });
      }
      for (const kw of diff.additions) {
        await api(`/categories/${categoryId}/keywords`, {
          method: "POST",
          body: JSON.stringify({ keyword: kw }),
        });
      }
      setOriginal(keywords);
      setEditing(false);
    } catch (e: any) {
      setError(e.message || "Failed to save changes");
    } finally {
      setBusy(false);
    }
  }

  function cancelEditing() {
    setKeywords(original);
    setInput("");
    setEditing(false);
  }

  if (loading) {
    return (
      <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
        <CircularProgress size={18} />
        <Typography variant="body2">Cargando palabras clave…</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Stack direction="row" spacing={1} alignItems="center" flexWrap="wrap" useFlexGap>
        {keywords.map((kw, idx) => (
          <Chip
            key={`${kw}-${idx}`}
            label={kw}
            onDelete={editing ? () => removeChip(idx) : undefined}
            variant={editing ? "filled" : "outlined"}
            sx={{ my: 0.5 }}
          />
        ))}
        {editing && (
          <TextField
            size="small"
            inputRef={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            onBlur={handleBlur}
            placeholder="Escribe y separa con coma…"
            sx={{ minWidth: 220, my: 0.5 }}
          />
        )}
        {editing && keywords.length === 0 && input.length === 0 && (
          <Chip icon={<AddIcon />} label="Agrega una palabra clave" variant="outlined" />
        )}
      </Stack>

      <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
        {!editing ? (
          <Tooltip title="Editar palabras clave">
            <span>
              <Button
                variant="contained"
                size="small"
                startIcon={<EditIcon />}
                onClick={() => {
                  setEditing(true);
                  setTimeout(() => inputRef.current?.focus(), 0);
                }}
              >
                Editar
              </Button>
            </span>
          </Tooltip>
        ) : (
          <>
            <Button
              variant="contained"
              color="success"
              size="small"
              startIcon={<SaveIcon />}
              onClick={saveChanges}
              disabled={busy || !diff.changed}
            >
              Guardar {busy && <CircularProgress size={14} sx={{ ml: 1 }} />}
            </Button>
            <Button variant="outlined" size="small" startIcon={<CloseIcon />} onClick={cancelEditing} disabled={busy}>
              Cancelar
            </Button>
            <Box sx={{ alignSelf: "center" }}>
              <Typography variant="caption" color="text.secondary">
                Sugerencia: presiona <kbd>Enter</kbd> o escribe una <b>,</b> para agregar un keyword.
              </Typography>
            </Box>
          </>
        )}
      </Stack>

      <Snackbar open={!!error} onClose={() => setError(null)} autoHideDuration={6000}>
        <Alert severity="error" variant="filled" onClose={() => setError(null)}>
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
}

// ===== Category List
function CategoryCard({ category }: { category: Category }) {
  return (
    <Card sx={{ borderRadius: 3, boxShadow: 2 }}>
      <CardHeader
        title={
          <Stack direction="row" spacing={1} alignItems="center">
            <Typography variant="h6">{category.emoji ? `${category.emoji} ` : ""}{category.name}</Typography>
            <Typography variant="body2" color="text.secondary">ID: {category.id}</Typography>
          </Stack>
        }
      />
      <CardContent>
        <EditableKeywords categoryId={category.id} />
      </CardContent>
    </Card>
  );
}

// ===== Main App
function App() {
  const [categories, setCategories] = useState<Category[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    api<Category[]>("/categories")
      .then((data) => {
        if (cancelled) return;
        setCategories(data);
      })
      .catch((e) => setError(e.message))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Stack spacing={2}>
        <Box>
          <Typography variant="h4" fontWeight={700}>Expense Bot — Keywords</Typography>
          <Typography variant="body1" color="text.secondary">
            Administra las palabras clave por categoría. Escribe varias y sepáralas con comas. Las palabras clave pueden contener espacios.
          </Typography>
          <Divider sx={{ mt: 2 }} />
        </Box>

        {loading && (
          <Stack direction="row" spacing={1} alignItems="center">
            <CircularProgress size={20} />
            <Typography>Cargando categorías…</Typography>
          </Stack>
        )}

        {error && (
          <Alert severity="error" variant="outlined">
            {error}
          </Alert>
        )}

        {!loading && categories && categories.length === 0 && (
          <Alert severity="info">No hay categorías todavía. Crea categorías desde el backend y recarga.</Alert>
        )}

        {!loading && categories && categories.map((cat) => <CategoryCard key={cat.id} category={cat} />)}

        <Box sx={{ mt: 4 }}>
          <Typography variant="caption" color="text.secondary">
            API base: <code>{API_BASE_URL}</code>
          </Typography>
        </Box>
      </Stack>
    </Container>
  );
}

// ===== Quick Usage Notes =====
// 1) Set API base URL via Vite: define VITE_API_BASE_URL in an .env file (e.g., http://localhost:8000)
// 2) Ensure CORS is enabled on FastAPI (e.g., CORSMiddleware allowing your dev origin)
// 3) Install deps: `npm i @mui/material @mui/icons-material @emotion/react @emotion/styled`
// 4) This component assumes the backend endpoints as documented in README.

export default App;

#ifndef SIMPLEDICTIONARY_H
#define SIMPLEDICTIONARY_H

template <typename K, typename V, int MAX_SIZE>
class SimpleDictionary {
public:
    SimpleDictionary() : size_(0) {}

    bool put(const K& key, const V& value) {
        int index = indexOf(key);
        if (index != -1) {
            values_[index] = value;
            Serial.print("Debug: Actualizando ");
            Serial.print(key);
            Serial.print(" con valor ");
            Serial.println(value);
            return true;
        }
        if (size_ < MAX_SIZE) {
            keys_[size_] = key;
            values_[size_] = value;
            ++size_;
            Serial.print("Debug: Insertando ");
            Serial.print(key);
            Serial.print(" con valor ");
            Serial.println(value);
            return true;
        }
        return false;
    }

    bool get(const K& key, V& value) const {
        int index = indexOf(key);
        if (index != -1) {
            value = values_[index];
            Serial.print("Debug: Obteniendo ");
            Serial.print(key);
            Serial.print(" con valor ");
            Serial.println(value);
            return true;
        }
        Serial.print("Debug: ");
        Serial.print(key);
        Serial.println(" no encontrado");
        return false;
    }

    bool contains(const K& key) const {
        return indexOf(key) != -1;
    }

    bool remove(const K& key) {
        int index = indexOf(key);
        if (index != -1) {
            for (int i = index; i < size_ - 1; ++i) {
                keys_[i] = keys_[i + 1];
                values_[i] = values_[i + 1];
            }
            --size_;
            return true;
        }
        return false;
    }

    int size() const {
        return size_;
    }

    void clear() {
        size_ = 0;
    }

private:
    int indexOf(const K& key) const {
        for (int i = 0; i < size_; ++i) {
            if (keys_[i] == key) {
                return i;
            }
        }
        return -1;
    }

    K keys_[MAX_SIZE];
    V values_[MAX_SIZE];
    int size_;
};

#endif // SIMPLEDICTIONARY_H

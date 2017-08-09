/*
 * <one line to give the library's name and an idea of what it does.>
 * Copyright (C) 2017  Aetf <aetf@unlimitedcodeworks.xyz>
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 */

#ifndef MEMORYMGR_H
#define MEMORYMGR_H

#include <cstddef>
#include <memory>

/**
 * @todo write docs
 */
class MemoryMgr
{
public:
    static MemoryMgr &instance();
    ~MemoryMgr();

    void *allocate(int alignment, size_t num_bytes);
    void deallocate(void *ptr);

private:
    MemoryMgr();
};

#endif // MEMORYMGR_H

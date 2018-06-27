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
 */

#ifndef SALUS_EXEC_SCHED_FAIR_H
#define SALUS_EXEC_SCHED_FAIR_H

#include "execution/scheduler/basescheduler.h"

#include <chrono>
#include <unordered_map>

/**
 * @todo write docs
 */
class FairScheduler : public BaseScheduler
{
public:
    explicit FairScheduler(salus::TaskExecutor &engine);
    ~FairScheduler() override;

    std::string name() const override;

    void notifyPreSchedulingIteration(const SessionList &sessions,
                                      const SessionChangeSet &changeset,
                                      sstl::not_null<CandidateList *> candidates) override;
    std::pair<size_t, bool> maybeScheduleFrom(PSessionItem item) override;

    using BaseScheduler::debugString;
    std::string debugString(const PSessionItem &item) const override;

private:
    std::pair<size_t, bool> reportScheduleResult(size_t scheduled) const;

    std::unordered_map<std::string, double> aggResUsages;
};

#endif // SALUS_EXEC_SCHED_FAIR_H
